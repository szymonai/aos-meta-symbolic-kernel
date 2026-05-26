from __future__ import annotations

import argparse
import gc
import importlib
import json
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

LATENCY_SCHEMA_VERSION = "latency-smoke/v1"
BENCHMARK_KIND = "local_latency_smoke_benchmark"

CLAIM_BOUNDARY = {
    "production_latency_claim": False,
    "production_sla_claim": False,
    "capacity_planning_claim": False,
    "availability_claim": False,
    "regulated_use_claim": False,
}

USEFULNESS = {
    "useful_for": [
        "local micro-latency inspection",
        "checking benchmark runner overhead trends",
        "detecting large public demonstrator latency regressions",
    ],
    "not_useful_for": [
        "production service-level agreement",
        "capacity planning",
        "availability validation",
        "regulated-use performance validation",
        "cross-machine performance comparison",
    ],
}


def percentile(samples: list[int], percentile_value: float) -> int:
    if not samples:
        raise ValueError("samples must not be empty")
    ordered = sorted(samples)
    index = round((len(ordered) - 1) * percentile_value / 100)
    return ordered[index]


def timer_overhead_ns(samples: int = 1000) -> int:
    measurements = []
    for _ in range(samples):
        start = time.perf_counter_ns()
        measurements.append(time.perf_counter_ns() - start)
    return int(statistics.median(measurements))


def summarize_ns(samples: list[int]) -> dict[str, float | int]:
    return {
        "sample_count": len(samples),
        "mean_us": round(statistics.fmean(samples) / 1_000, 6),
        "median_us": round(statistics.median(samples) / 1_000, 6),
        "p95_us": round(percentile(samples, 95) / 1_000, 6),
        "p99_us": round(percentile(samples, 99) / 1_000, 6),
        "max_us": round(max(samples) / 1_000, 6),
    }


def measure_guard(
    name: str,
    module_path: str,
    scenarios: list[dict[str, Any]],
    *,
    iterations: int,
    warmup: int,
) -> dict[str, Any]:
    module = importlib.import_module(module_path)

    for _ in range(warmup):
        for scenario in scenarios:
            module.evaluate(scenario)

    samples = []
    gc_was_enabled = gc.isenabled()
    if gc_was_enabled:
        gc.disable()
    try:
        total_start = time.perf_counter_ns()
        for _ in range(iterations):
            for scenario in scenarios:
                start = time.perf_counter_ns()
                module.evaluate(scenario)
                samples.append(time.perf_counter_ns() - start)
        total_ns = time.perf_counter_ns() - total_start
    finally:
        if gc_was_enabled:
            gc.enable()

    summary = summarize_ns(samples)
    summary.update(
        {
            "name": name,
            "iterations": iterations,
            "scenario_count": len(scenarios),
            "total_ms": round(total_ns / 1_000_000, 6),
        }
    )
    return summary


def build_latency_metrics(iterations: int = 1000, warmup: int = 100) -> dict[str, Any]:
    from benchmarks.run_benchmarks import BASELINES, load_scenarios

    if iterations < 1:
        raise ValueError("iterations must be positive")
    if warmup < 0:
        raise ValueError("warmup must be non-negative")

    scenarios = load_scenarios()
    return {
        "schema_version": LATENCY_SCHEMA_VERSION,
        "benchmark_metadata": {
            "benchmark_kind": BENCHMARK_KIND,
            "primary_use": "local_public_demonstrator_latency_smoke",
            "scenario_source": "benchmarks/scenarios.json",
            "timer": "time.perf_counter_ns",
            "timer_overhead_median_ns": timer_overhead_ns(),
            "iterations_per_guard": iterations,
            "warmup_iterations_per_guard": warmup,
        },
        "environment": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "system": platform.system(),
            "machine": platform.machine(),
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "usefulness_verification": USEFULNESS,
        "scenario_count": len(scenarios),
        "guards": [
            measure_guard(
                name,
                module_path,
                scenarios,
                iterations=iterations,
                warmup=warmup,
            )
            for name, module_path in BASELINES.items()
        ],
    }


def metrics_to_json(metrics: dict[str, Any]) -> str:
    return json.dumps(metrics, allow_nan=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--warmup", type=int, default=100)
    parser.add_argument(
        "--output",
        type=Path,
        help="optional path for a local, environment-specific latency report",
    )
    args = parser.parse_args(argv)

    metrics = build_latency_metrics(iterations=args.iterations, warmup=args.warmup)
    payload = metrics_to_json(metrics)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

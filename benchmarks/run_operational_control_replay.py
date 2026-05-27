from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.aos_public_core import (  # noqa: E402
    build_signal_evidence,
    canonical_json_bytes,
    parse_signal,
    verify_signal_evidence,
)

DEFAULT_NAB_ROOT = REPO_ROOT / "data" / "external" / "NAB"
RESULTS_DIR = ROOT / "results"
METRICS_PATH = RESULTS_DIR / "operational_control_replay_metrics.json"
SUMMARY_PATH = RESULTS_DIR / "operational_control_replay_summary.md"

SCHEMA_VERSION = "operational-control-replay/v1"
BENCHMARK_KIND = "public_operational_shadow_replay"
POLICY_ID = "nab_operational_replay_v1"
POLICY_VERSION = "0.1.0"
DEFAULT_LIMIT = 7000
DEFAULT_WARN_MARGIN = 2000
DEFAULT_ROLLING_WINDOW = 48
DEFAULT_MIN_HISTORY = 48
ROBUST_Z_AT_FULL_SCALE = 6.0

GUARDS = ("pass_through_baseline", "block_only_score_baseline", "aos_control_gate")

CLAIM_BOUNDARY = {
    "production_deployment_claim": False,
    "production_sla_claim": False,
    "regulated_use_claim": False,
    "domain_validation_claim": False,
    "external_validation_claim": False,
    "general_aos_effectiveness_claim": False,
    "anomaly_detector_superiority_claim": False,
    "dataset_redistribution_claim": False,
}

USEFULNESS_VERIFICATION = {
    "useful_for": [
        "offline shadow-mode replay on public operational time-series data",
        "measuring silent anomaly pass-through under a fixed public policy",
        "checking deterministic replay and local audit evidence coverage",
        "comparing review-band control against pass-through and block-only baselines",
    ],
    "not_useful_for": [
        "production deployment proof",
        "service-level agreement",
        "regulated-use approval",
        "ranking anomaly-detection models",
        "external validation",
        "domain-specific safety approval",
    ],
}

PRODUCTION_RELEVANCE_PROFILE = {
    "claim_type": "production_relevant_offline_replay",
    "production_deployment_claim": False,
    "public_operational_data": True,
    "offline_shadow_mode": True,
    "fixed_policy": True,
    "fixed_signal_extractor": True,
    "labels_used_as_aos_input_signals": False,
    "why_relevant": [
        "public operational traces are replayed record by record",
        "the policy routes records to PASS, WARN, or BLOCK before downstream action",
        "the benchmark measures silent pass-through and intervention load",
        "AOS decisions produce replayable audit evidence",
    ],
    "why_not_production_proof": [
        "no live traffic",
        "no deployed service boundary",
        "no service-level objective",
        "no operator workflow validation",
        "no external validation",
    ],
}

FALSIFICATION_PROFILE = {
    "falsifiable_claim": (
        "For the pinned public dataset, policy, and code path, the committed "
        "operational replay artifacts reproduce and AOS audit evidence replays."
    ),
    "check_command": "python benchmarks/run_operational_control_replay.py --check",
    "falsification_conditions": [
        "committed metrics or summary drift under the same dataset and code",
        "AOS audit coverage falls below 100% for evaluated records",
        "AOS replay success falls below 100% for evaluated records",
        "labels are used as AOS input signals",
        "claim-boundary flags are changed to production or regulated-use claims",
        "aggregate decision stream hash changes without artifact update",
    ],
    "reported_tradeoffs": [
        "anomaly-window silent pass rate",
        "anomaly-window review/block rate",
        "record-level anomaly review/block rate",
        "false block rate",
        "nominal intervention rate",
    ],
}


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics_to_json(metrics: dict[str, Any]) -> str:
    return json.dumps(metrics, allow_nan=False, indent=2, sort_keys=True) + "\n"


def safe_rate(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


def percentile(values: list[int], percentile_value: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = round((len(ordered) - 1) * percentile_value / 100)
    return ordered[index]


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.strip())


def load_json_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def load_windows(nab_root: Path) -> dict[str, list[tuple[datetime, datetime]]]:
    labels_path = nab_root / "labels" / "combined_windows.json"
    payload = load_json_object(labels_path)
    windows: dict[str, list[tuple[datetime, datetime]]] = {}
    for relative_path, entries in payload.items():
        if not isinstance(relative_path, str) or not isinstance(entries, list):
            raise ValueError("NAB window labels have unexpected shape")
        parsed_entries = []
        for entry in entries:
            if (
                not isinstance(entry, list)
                or len(entry) != 2
                or not all(isinstance(item, str) for item in entry)
            ):
                raise ValueError(f"invalid NAB window entry for {relative_path}")
            parsed_entries.append(
                (parse_timestamp(entry[0]), parse_timestamp(entry[1]))
            )
        windows[relative_path] = parsed_entries
    return windows


def load_series(path: Path) -> list[tuple[datetime, float]]:
    rows: list[tuple[datetime, float]] = []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["timestamp", "value"]:
            raise ValueError(f"unexpected NAB CSV header in {path}")
        for row in reader:
            rows.append((parse_timestamp(row["timestamp"]), float(row["value"])))
    return rows


def dataset_commit(nab_root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(nab_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    commit = result.stdout.strip()
    return commit or None


def in_any_window(
    timestamp: datetime,
    windows: list[tuple[datetime, datetime]],
) -> bool:
    return any(start <= timestamp <= end for start, end in windows)


def window_indexes_for(
    timestamp: datetime,
    windows: list[tuple[datetime, datetime]],
) -> list[int]:
    return [
        index
        for index, (start, end) in enumerate(windows)
        if start <= timestamp <= end
    ]


def robust_scale(history: list[float], center: float) -> float:
    deviations = [abs(value - center) for value in history]
    mad = statistics.median(deviations)
    if mad > 0:
        return max(1e-9, 1.4826 * mad)
    mean_abs = statistics.fmean(deviations) if deviations else 0.0
    return max(1e-9, mean_abs)


def risk_score(value: float, history: list[float]) -> int:
    center = statistics.median(history)
    scale = robust_scale(history, center)
    robust_z = abs(value - center) / scale
    change_z = abs(value - history[-1]) / scale
    risk_z = max(robust_z, change_z)
    score = round((risk_z / ROBUST_Z_AT_FULL_SCALE) * 10_000)
    return max(0, min(10_000, score))


def signal_payload(
    *,
    relative_path: str,
    index: int,
    timestamp: datetime,
    score: int,
    limit: int,
    warn_margin: int,
) -> dict[str, Any]:
    return {
        "signal_id": f"nab:{relative_path}:{index}:{timestamp.isoformat()}",
        "score": score,
        "uncertainty": 0,
        "limit": limit,
        "warn_margin": warn_margin,
        "metadata_complete": True,
        "policy_id": POLICY_ID,
        "policy_version": POLICY_VERSION,
    }


def verdict_for_guard(
    guard_name: str,
    payload: dict[str, Any],
) -> tuple[str, str | None, bool]:
    if guard_name == "pass_through_baseline":
        return "PASS", None, False
    if guard_name == "block_only_score_baseline":
        return ("BLOCK" if payload["score"] > payload["limit"] else "PASS"), None, False
    if guard_name != "aos_control_gate":
        raise ValueError(f"unknown guard: {guard_name}")

    evidence = asdict(build_signal_evidence(parse_signal(payload)))
    replay = verify_signal_evidence(evidence)
    return str(evidence["verdict"]), str(evidence["audit_id"]), bool(replay["valid"])


def empty_guard_metrics(name: str) -> dict[str, Any]:
    return {
        "name": name,
        "record_count": 0,
        "anomaly_count": 0,
        "nominal_count": 0,
        "pass_count": 0,
        "warn_count": 0,
        "block_count": 0,
        "anomaly_pass_count": 0,
        "anomaly_warn_count": 0,
        "anomaly_block_count": 0,
        "nominal_pass_count": 0,
        "nominal_warn_count": 0,
        "nominal_block_count": 0,
        "audit_record_count": 0,
        "replay_success_count": 0,
        "anomaly_window_count": 0,
        "anomaly_window_review_or_block_count": 0,
        "anomaly_window_block_count": 0,
    }


def update_guard_metrics(
    metrics: dict[str, Any],
    *,
    is_anomaly: bool,
    verdict: str,
    audit_id: str | None,
    replay_valid: bool,
) -> None:
    metrics["record_count"] += 1
    metrics[f"{verdict.casefold()}_count"] += 1
    if is_anomaly:
        metrics["anomaly_count"] += 1
        metrics[f"anomaly_{verdict.casefold()}_count"] += 1
    else:
        metrics["nominal_count"] += 1
        metrics[f"nominal_{verdict.casefold()}_count"] += 1
    if audit_id:
        metrics["audit_record_count"] += 1
    if replay_valid:
        metrics["replay_success_count"] += 1


def finalize_guard_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    anomaly_count = int(metrics["anomaly_count"])
    nominal_count = int(metrics["nominal_count"])
    record_count = int(metrics["record_count"])
    anomaly_window_count = int(metrics["anomaly_window_count"])
    anomaly_review_or_block = int(metrics["anomaly_warn_count"]) + int(
        metrics["anomaly_block_count"]
    )
    nominal_interventions = int(metrics["nominal_warn_count"]) + int(
        metrics["nominal_block_count"]
    )
    return {
        **metrics,
        "silent_anomaly_pass_rate": safe_rate(
            int(metrics["anomaly_pass_count"]),
            anomaly_count,
        ),
        "anomaly_review_or_block_rate": safe_rate(
            anomaly_review_or_block,
            anomaly_count,
        ),
        "anomaly_block_rate": safe_rate(
            int(metrics["anomaly_block_count"]),
            anomaly_count,
        ),
        "nominal_pass_rate": safe_rate(
            int(metrics["nominal_pass_count"]),
            nominal_count,
        ),
        "false_block_rate": safe_rate(
            int(metrics["nominal_block_count"]),
            nominal_count,
        ),
        "nominal_intervention_rate": safe_rate(nominal_interventions, nominal_count),
        "warn_review_load_rate": safe_rate(int(metrics["warn_count"]), record_count),
        "block_load_rate": safe_rate(int(metrics["block_count"]), record_count),
        "audit_coverage_rate": safe_rate(
            int(metrics["audit_record_count"]),
            record_count,
        ),
        "replay_success_rate": safe_rate(
            int(metrics["replay_success_count"]),
            record_count,
        ),
        "anomaly_window_silent_pass_rate": safe_rate(
            anomaly_window_count - int(metrics["anomaly_window_review_or_block_count"]),
            anomaly_window_count,
        ),
        "anomaly_window_review_or_block_rate": safe_rate(
            int(metrics["anomaly_window_review_or_block_count"]),
            anomaly_window_count,
        ),
        "anomaly_window_block_rate": safe_rate(
            int(metrics["anomaly_window_block_count"]),
            anomaly_window_count,
        ),
    }


def summarize_scores(scores: list[int]) -> dict[str, int | float]:
    if not scores:
        return {"min": 0, "median": 0.0, "p95": 0, "p99": 0, "max": 0}
    return {
        "min": min(scores),
        "median": round(float(statistics.median(scores)), 6),
        "p95": percentile(scores, 95),
        "p99": percentile(scores, 99),
        "max": max(scores),
    }


def evaluate_series(
    *,
    nab_root: Path,
    relative_path: str,
    windows: list[tuple[datetime, datetime]],
    rolling_window: int,
    min_history: int,
    limit: int,
    warn_margin: int,
) -> dict[str, Any]:
    series_path = nab_root / "data" / relative_path
    rows = load_series(series_path)
    guard_metrics = {name: empty_guard_metrics(name) for name in GUARDS}
    window_hits = {
        name: [
            {"review_or_block": False, "block": False}
            for _ in range(len(windows))
        ]
        for name in GUARDS
    }
    decision_hash = hashlib.sha256()
    scores: list[int] = []
    skipped_warmup = 0

    for index, (timestamp, value) in enumerate(rows):
        history_start = max(0, index - rolling_window)
        history_values = [item[1] for item in rows[history_start:index]]
        if len(history_values) < min_history:
            skipped_warmup += 1
            continue

        score = risk_score(value, history_values)
        scores.append(score)
        payload = signal_payload(
            relative_path=relative_path,
            index=index,
            timestamp=timestamp,
            score=score,
            limit=limit,
            warn_margin=warn_margin,
        )
        window_indexes = window_indexes_for(timestamp, windows)
        is_anomaly = bool(window_indexes)
        decision_material: dict[str, Any] = {
            "index": index,
            "is_anomaly": is_anomaly,
            "score": score,
            "timestamp": timestamp.isoformat(),
        }

        for guard_name, metrics in guard_metrics.items():
            verdict, audit_id, replay_valid = verdict_for_guard(guard_name, payload)
            update_guard_metrics(
                metrics,
                is_anomaly=is_anomaly,
                verdict=verdict,
                audit_id=audit_id,
                replay_valid=replay_valid,
            )
            decision_material[guard_name] = {
                "audit_id": audit_id,
                "verdict": verdict,
            }
            for window_index in window_indexes:
                if verdict in {"WARN", "BLOCK"}:
                    window_hits[guard_name][window_index]["review_or_block"] = True
                if verdict == "BLOCK":
                    window_hits[guard_name][window_index]["block"] = True

        decision_hash.update(canonical_json_bytes(decision_material))

    for guard_name, hits in window_hits.items():
        metrics = guard_metrics[guard_name]
        metrics["anomaly_window_count"] = len(hits)
        metrics["anomaly_window_review_or_block_count"] = sum(
            bool(item["review_or_block"]) for item in hits
        )
        metrics["anomaly_window_block_count"] = sum(
            bool(item["block"]) for item in hits
        )

    return {
        "path": relative_path,
        "source_sha256": sha256_file(series_path),
        "record_count": len(rows),
        "evaluated_count": len(scores),
        "skipped_warmup_count": skipped_warmup,
        "window_count": len(windows),
        "score_summary": summarize_scores(scores),
        "guards": {
            name: finalize_guard_metrics(metrics)
            for name, metrics in guard_metrics.items()
        },
        "decision_stream_sha256": decision_hash.hexdigest(),
    }


def merge_guard_metrics(series_metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = {name: empty_guard_metrics(name) for name in GUARDS}
    for series in series_metrics:
        guards = series["guards"]
        for guard_name, target in merged.items():
            source = guards[guard_name]
            for key, value in source.items():
                if isinstance(value, int):
                    target[key] += value
    return [finalize_guard_metrics(merged[name]) for name in GUARDS]


def scalability_profile(
    *,
    series_count: int,
    evaluated_record_count: int,
    anomaly_window_count: int,
    rolling_window: int,
) -> dict[str, Any]:
    return {
        "scale_unit": "evaluated_records",
        "series_count": series_count,
        "evaluated_record_count": evaluated_record_count,
        "anomaly_window_count": anomaly_window_count,
        "gate_complexity_per_signal": "O(1)",
        "extractor_complexity": (
            "O(records * rolling_window log rolling_window); practical linear "
            "for fixed rolling_window"
        ),
        "rolling_window": rolling_window,
        "streaming_shape": "series-by-series replay with bounded rolling history",
        "not_claimed": [
            "distributed throughput",
            "production latency",
            "availability",
            "capacity planning",
            "GPU acceleration",
        ],
    }


def auditability_profile(
    *,
    aggregate_decision_stream_sha256: str,
    evaluated_record_count: int,
) -> dict[str, Any]:
    return {
        "audit_scope": "local demonstrator replay evidence",
        "aos_audit_record_expected_per_evaluated_record": True,
        "aos_replay_expected_per_evaluated_record": True,
        "evaluated_record_count": evaluated_record_count,
        "aggregate_decision_stream_sha256": aggregate_decision_stream_sha256,
        "per_series_source_sha256": True,
        "per_series_decision_stream_sha256": True,
        "not_claimed": [
            "production signing infrastructure",
            "immutable ledger",
            "key-management design",
            "non-repudiation",
        ],
    }


def build_metrics(
    *,
    nab_root: Path = DEFAULT_NAB_ROOT,
    rolling_window: int = DEFAULT_ROLLING_WINDOW,
    min_history: int = DEFAULT_MIN_HISTORY,
    limit: int = DEFAULT_LIMIT,
    warn_margin: int = DEFAULT_WARN_MARGIN,
    max_series: int | None = None,
) -> dict[str, Any]:
    if rolling_window < 2:
        raise ValueError("rolling_window must be at least 2")
    if min_history < 2:
        raise ValueError("min_history must be at least 2")
    if min_history > rolling_window:
        raise ValueError("min_history must not exceed rolling_window")
    if warn_margin >= limit:
        raise ValueError("warn_margin must be lower than limit")

    labels_path = nab_root / "labels" / "combined_windows.json"
    data_root = nab_root / "data"
    if not labels_path.is_file() or not data_root.is_dir():
        raise FileNotFoundError(
            "NAB dataset not found. Expected data and labels under "
            f"{nab_root}. Download with: git clone --depth 1 "
            "https://github.com/numenta/NAB.git data/external/NAB"
        )

    windows_by_path = load_windows(nab_root)
    selected_paths = sorted(windows_by_path)
    if max_series is not None:
        selected_paths = selected_paths[:max_series]

    series = [
        evaluate_series(
            nab_root=nab_root,
            relative_path=relative_path,
            windows=windows_by_path[relative_path],
            rolling_window=rolling_window,
            min_history=min_history,
            limit=limit,
            warn_margin=warn_margin,
        )
        for relative_path in selected_paths
    ]
    aggregate_hash = canonical_json_sha256(
        [
            {
                "decision_stream_sha256": item["decision_stream_sha256"],
                "path": item["path"],
            }
            for item in series
        ]
    )
    evaluated_record_count = sum(item["evaluated_count"] for item in series)
    anomaly_window_count = sum(item["window_count"] for item in series)

    return {
        "schema_version": SCHEMA_VERSION,
        "benchmark_metadata": {
            "benchmark_kind": BENCHMARK_KIND,
            "primary_use": "production_relevant_offline_shadow_replay",
            "dataset": "Numenta Anomaly Benchmark",
            "dataset_repository": "https://github.com/numenta/NAB",
            "dataset_commit": dataset_commit(nab_root),
            "dataset_license": "MIT",
            "dataset_redistributed_in_repo": False,
            "labels_source": "labels/combined_windows.json",
            "labels_sha256": sha256_file(labels_path),
            "policy_under_test": (
                "rolling robust anomaly score; PASS/WARN/BLOCK with warning band"
            ),
            "rolling_window": rolling_window,
            "min_history": min_history,
            "limit": limit,
            "warn_margin": warn_margin,
            "risk_score_scale": "0..10000",
            "result_artifacts": [
                "benchmarks/results/operational_control_replay_metrics.json",
                "benchmarks/results/operational_control_replay_summary.md",
            ],
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "usefulness_verification": USEFULNESS_VERIFICATION,
        "production_relevance_profile": PRODUCTION_RELEVANCE_PROFILE,
        "series_count": len(series),
        "source_series_count": len(windows_by_path),
        "evaluated_record_count": evaluated_record_count,
        "skipped_warmup_count": sum(item["skipped_warmup_count"] for item in series),
        "anomaly_window_count": anomaly_window_count,
        "aggregate_decision_stream_sha256": aggregate_hash,
        "scalability_profile": scalability_profile(
            series_count=len(series),
            evaluated_record_count=evaluated_record_count,
            anomaly_window_count=anomaly_window_count,
            rolling_window=rolling_window,
        ),
        "auditability_profile": auditability_profile(
            aggregate_decision_stream_sha256=aggregate_hash,
            evaluated_record_count=evaluated_record_count,
        ),
        "falsification_profile": FALSIFICATION_PROFILE,
        "guards": merge_guard_metrics(series),
        "series": series,
    }


def build_summary(metrics: dict[str, Any]) -> str:
    metadata = metrics["benchmark_metadata"]
    usefulness = metrics["usefulness_verification"]
    production_relevance = metrics["production_relevance_profile"]
    scalability = metrics["scalability_profile"]
    falsification = metrics["falsification_profile"]
    rows = [
        (
            "| Guard | Window silent pass | Window review/block | "
            "Record review/block | False block | Nominal intervention | "
            "Audit | Replay |"
        ),
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for guard in metrics["guards"]:
        rows.append(
            "| {name} | {anomaly_window_silent_pass_rate:.2%} | "
            "{anomaly_window_review_or_block_rate:.2%} | "
            "{anomaly_review_or_block_rate:.2%} | {false_block_rate:.2%} | "
            "{nominal_intervention_rate:.2%} | {audit_coverage_rate:.2%} | "
            "{replay_success_rate:.2%} |".format(**guard)
        )

    return "\n".join(
        [
            "# Operational Control Replay Summary",
            "",
            "This benchmark replays public time-series traces through a fixed AOS",
            "control policy. It measures whether labeled anomaly windows pass",
            "silently, route to review, or block. It is an offline shadow-mode",
            "benchmark, not a production deployment proof.",
            "",
            "Source:",
            "",
            f"- dataset: `{metadata['dataset']}`",
            f"- repository: `{metadata['dataset_repository']}`",
            f"- commit: `{metadata['dataset_commit']}`",
            f"- license: `{metadata['dataset_license']}`",
            f"- labels SHA-256: `{metadata['labels_sha256']}`",
            "",
            "Protocol:",
            "",
            f"- benchmark kind: `{metadata['benchmark_kind']}`",
            f"- primary use: `{metadata['primary_use']}`",
            f"- rolling window: `{metadata['rolling_window']}`",
            f"- minimum history: `{metadata['min_history']}`",
            f"- limit: `{metadata['limit']}`",
            f"- warning margin: `{metadata['warn_margin']}`",
            f"- evaluated records: `{metrics['evaluated_record_count']}`",
            f"- anomaly windows: `{metrics['anomaly_window_count']}`",
            "- aggregate decision SHA-256: "
            f"`{metrics['aggregate_decision_stream_sha256']}`",
            "",
            "Production-Relevant Proof Profile:",
            "",
            f"- claim type: `{production_relevance['claim_type']}`",
            "- public operational data: "
            f"`{production_relevance['public_operational_data']}`",
            f"- offline shadow mode: `{production_relevance['offline_shadow_mode']}`",
            f"- fixed policy: `{production_relevance['fixed_policy']}`",
            "- labels used as AOS input signals: "
            f"`{production_relevance['labels_used_as_aos_input_signals']}`",
            "",
            "Scalability Profile:",
            "",
            f"- scale unit: `{scalability['scale_unit']}`",
            "- gate complexity per signal: "
            f"`{scalability['gate_complexity_per_signal']}`",
            f"- extractor complexity: `{scalability['extractor_complexity']}`",
            f"- streaming shape: `{scalability['streaming_shape']}`",
            "",
            "Useful for:",
            "",
            *(f"- `{item}`" for item in usefulness["useful_for"]),
            "",
            "Not useful for:",
            "",
            *(f"- `{item}`" for item in usefulness["not_useful_for"]),
            "",
            *rows,
            "",
            "Interpretation:",
            "",
            "- `anomaly_window_silent_pass_rate` is the share of labeled anomaly",
            "  windows with no `WARN` or `BLOCK` decision.",
            "- `anomaly_window_review_or_block_rate` is the share of labeled anomaly",
            "  windows with at least one `WARN` or `BLOCK` decision.",
            "- `anomaly_review_or_block_rate` is the share of anomaly-window records",
            "  routed to `WARN` or `BLOCK`; this is secondary because NAB labels",
            "  anomaly windows rather than every point as an incident.",
            "- `false_block_rate` is the share of nominal records blocked.",
            "- `nominal_intervention_rate` is the share of nominal records routed to",
            "  `WARN` or `BLOCK`.",
            "- `audit_coverage_rate` and `replay_success_rate` are local demonstrator",
            "  evidence checks for the AOS guard.",
            "",
            "Falsification Criteria:",
            "",
            f"- claim: `{falsification['falsifiable_claim']}`",
            f"- check command: `{falsification['check_command']}`",
            *(f"- fail if: `{item}`" for item in falsification[
                "falsification_conditions"
            ]),
            "",
            "Boundary:",
            "",
            "The score extractor is deterministic and label-independent, but it is",
            "not a claim that AOS is an anomaly detector. The result is production-",
            "relevant control evidence over public frozen traces.",
        ]
    )


def run(
    *,
    nab_root: Path = DEFAULT_NAB_ROOT,
    write: bool = True,
    max_series: int | None = None,
) -> dict[str, Any]:
    metrics = build_metrics(nab_root=nab_root, max_series=max_series)
    if not write:
        return metrics
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(metrics_to_json(metrics), encoding="utf-8")
    SUMMARY_PATH.write_text(build_summary(metrics) + "\n", encoding="utf-8")
    return metrics


def guard_metrics_by_name(
    metrics: dict[str, Any],
    name: str,
) -> dict[str, Any]:
    guards = metrics.get("guards")
    if not isinstance(guards, list):
        raise SystemExit("operational control replay guards must be a list")
    for guard in guards:
        if isinstance(guard, dict) and guard.get("name") == name:
            return guard
    raise SystemExit(f"missing operational control replay guard: {name}")


def validate_committed_artifacts() -> None:
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    if metrics.get("schema_version") != SCHEMA_VERSION:
        raise SystemExit("operational control replay metrics schema mismatch")
    production_claim = metrics.get("claim_boundary", {}).get(
        "production_deployment_claim"
    )
    if production_claim is not False:
        raise SystemExit("production deployment claim must remain false")
    if not SUMMARY_PATH.is_file():
        raise SystemExit("missing operational control replay summary")
    summary = SUMMARY_PATH.read_text(encoding="utf-8")
    for heading in ("Production-Relevant Proof Profile", "Falsification Criteria"):
        if heading not in summary:
            raise SystemExit(f"operational replay summary missing: {heading}")

    required_profiles = (
        "production_relevance_profile",
        "scalability_profile",
        "auditability_profile",
        "falsification_profile",
    )
    for profile in required_profiles:
        if not isinstance(metrics.get(profile), dict):
            raise SystemExit(f"operational replay metrics missing {profile}")

    production_relevance = metrics["production_relevance_profile"]
    if production_relevance.get("claim_type") != "production_relevant_offline_replay":
        raise SystemExit("unexpected operational replay claim type")
    if production_relevance.get("production_deployment_claim") is not False:
        raise SystemExit("operational replay must not claim production deployment")
    if production_relevance.get("labels_used_as_aos_input_signals") is not False:
        raise SystemExit("operational replay must not use labels as AOS inputs")

    scalability = metrics["scalability_profile"]
    if scalability.get("series_count") != metrics.get("series_count"):
        raise SystemExit("operational replay scalability series count mismatch")
    if scalability.get("evaluated_record_count") != metrics.get(
        "evaluated_record_count"
    ):
        raise SystemExit("operational replay scalability record count mismatch")
    if scalability.get("gate_complexity_per_signal") != "O(1)":
        raise SystemExit("operational replay gate complexity profile changed")

    auditability = metrics["auditability_profile"]
    if auditability.get("aggregate_decision_stream_sha256") != metrics.get(
        "aggregate_decision_stream_sha256"
    ):
        raise SystemExit("operational replay aggregate decision hash mismatch")
    if auditability.get("aos_audit_record_expected_per_evaluated_record") is not True:
        raise SystemExit("operational replay audit expectation missing")
    if auditability.get("aos_replay_expected_per_evaluated_record") is not True:
        raise SystemExit("operational replay replay expectation missing")

    falsification = metrics["falsification_profile"]
    if falsification.get("check_command") != (
        "python benchmarks/run_operational_control_replay.py --check"
    ):
        raise SystemExit("operational replay falsification command mismatch")
    conditions = falsification.get("falsification_conditions")
    if not isinstance(conditions, list) or len(conditions) < 5:
        raise SystemExit("operational replay falsification criteria are too weak")

    if int(metrics.get("series_count", 0)) < 50:
        raise SystemExit("operational replay series scale is below public threshold")
    if int(metrics.get("evaluated_record_count", 0)) < 100_000:
        raise SystemExit("operational replay record scale is below public threshold")
    if int(metrics.get("anomaly_window_count", 0)) < 100:
        raise SystemExit("operational replay anomaly-window scale is below threshold")

    aos = guard_metrics_by_name(metrics, "aos_control_gate")
    if aos.get("audit_coverage_rate") != 1.0:
        raise SystemExit("AOS audit coverage must remain 100% in committed replay")
    if aos.get("replay_success_rate") != 1.0:
        raise SystemExit("AOS replay success must remain 100% in committed replay")
    if float(aos.get("anomaly_window_review_or_block_rate", 0.0)) < 0.9:
        raise SystemExit("AOS anomaly-window review/block rate below threshold")
    if float(aos.get("anomaly_window_silent_pass_rate", 1.0)) > 0.1:
        raise SystemExit("AOS anomaly-window silent pass rate above threshold")


def check_committed_results(nab_root: Path) -> None:
    if not (nab_root / "labels" / "combined_windows.json").is_file():
        validate_committed_artifacts()
        return

    metrics = run(nab_root=nab_root, write=False)
    expected = {
        METRICS_PATH: metrics_to_json(metrics),
        SUMMARY_PATH: build_summary(metrics) + "\n",
    }
    mismatches = [
        path
        for path, expected_content in expected.items()
        if path.read_text(encoding="utf-8") != expected_content
    ]
    if mismatches:
        files = ", ".join(str(path.relative_to(REPO_ROOT)) for path in mismatches)
        raise SystemExit(
            "Operational control replay result drift detected in "
            f"{files}. Run `python benchmarks/run_operational_control_replay.py` "
            "with the NAB dataset available and commit the updated artifacts."
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nab-root", type=Path, default=DEFAULT_NAB_ROOT)
    parser.add_argument("--max-series", type=int)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed artifacts; regenerate when local NAB data exists",
    )
    args = parser.parse_args(argv)

    if args.check:
        check_committed_results(args.nab_root)
        return 0

    run(nab_root=args.nab_root, max_series=args.max_series)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

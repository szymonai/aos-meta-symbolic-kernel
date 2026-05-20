from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import gradio as gr

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.aos_public_core import DemoIntervalGate  # noqa: E402


def evaluate(
    value: float,
    uncertainty: float,
    limit: float,
    warn_margin: float,
) -> tuple[str, dict[str, Any], str]:
    try:
        gate = DemoIntervalGate(limit=limit, warn_margin=warn_margin)
        record = gate.evaluate(
            value=value,
            uncertainty=uncertainty,
        )
        evidence = {
            "schema_version": "aos-gradio-sandbox/v1",
            "verdict": record.verdict,
            "audit_id": f"sha256:{record.audit_digest}",
            "input": {
                "value": record.value,
                "uncertainty": record.uncertainty,
                "limit": record.limit,
                "warn_margin": warn_margin,
            },
            "claim_boundary": {
                "production_use_claim": False,
                "domain_validation_claim": False,
                "regulated_use_claim": False,
            },
        }
        return record.verdict, evidence, json.dumps(evidence, sort_keys=True)
    except Exception as exc:
        evidence = {
            "schema_version": "aos-gradio-sandbox/v1",
            "verdict": "BLOCK",
            "error": str(exc),
            "claim_boundary": {
                "production_use_claim": False,
                "domain_validation_claim": False,
                "regulated_use_claim": False,
            },
        }
        return "BLOCK", evidence, json.dumps(evidence, sort_keys=True)


with gr.Blocks(title="AOS Public Sandbox") as demo:
    gr.Markdown("# AOS Public Sandbox")
    with gr.Row():
        value = gr.Slider(0, 100, value=40, step=1, label="Value")
        uncertainty = gr.Slider(0, 50, value=5, step=1, label="Uncertainty")
    with gr.Row():
        limit = gr.Slider(1, 100, value=60, step=1, label="Limit")
        warn_margin = gr.Slider(0, 50, value=10, step=1, label="Warn margin")

    run = gr.Button("Evaluate", variant="primary")
    verdict = gr.Textbox(label="Verdict", interactive=False)
    evidence = gr.JSON(label="Evidence")
    canonical = gr.Textbox(label="Canonical evidence", lines=4, interactive=False)

    run.click(
        fn=evaluate,
        inputs=[value, uncertainty, limit, warn_margin],
        outputs=[verdict, evidence, canonical],
        api_name="evaluate",
    )


if __name__ == "__main__":
    demo.launch()

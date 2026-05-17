from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Literal, TypeAlias
from urllib.parse import urlparse

SCORE_SCALE = 10_000
MAX_BODY_BYTES = 64 * 1024
DEFAULT_POLICY_ID = "demo_gate_policy_v1"
DEFAULT_POLICY_VERSION = "1.0.0"

Verdict: TypeAlias = Literal["PASS", "WARN", "BLOCK"]


@dataclass(frozen=True, slots=True)
class DemoSignal:
    signal_id: str
    score: int
    uncertainty: int
    limit: int
    warn_margin: int
    metadata_complete: bool
    policy_id: str = DEFAULT_POLICY_ID
    policy_version: str = DEFAULT_POLICY_VERSION


@dataclass(frozen=True, slots=True)
class DemoEvidence:
    schema_version: str
    signal_id: str
    verdict: Verdict
    reason: str
    audit_id: str
    input_digest: str
    policy_id: str
    policy_version: str
    replayable: bool
    claim_boundary: dict[str, bool]
    input: dict[str, Any]


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_tag(value: Any) -> str:
    digest = hashlib.sha256(canonical_json_bytes(value)).hexdigest()
    return f"sha256:{digest}"


def require_nat(name: str, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def require_text(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def parse_signal(payload: dict[str, Any]) -> DemoSignal:
    required = (
        "signal_id",
        "score",
        "uncertainty",
        "limit",
        "warn_margin",
        "metadata_complete",
    )
    for field in required:
        if field not in payload:
            raise ValueError(f"missing required field: {field}")

    metadata_complete = payload["metadata_complete"]
    if not isinstance(metadata_complete, bool):
        raise ValueError("metadata_complete must be boolean")

    signal = DemoSignal(
        signal_id=require_text("signal_id", payload["signal_id"]),
        score=require_nat("score", payload["score"]),
        uncertainty=require_nat("uncertainty", payload["uncertainty"]),
        limit=require_nat("limit", payload["limit"]),
        warn_margin=require_nat("warn_margin", payload["warn_margin"]),
        metadata_complete=metadata_complete,
        policy_id=require_text(
            "policy_id",
            payload.get("policy_id", DEFAULT_POLICY_ID),
        ),
        policy_version=require_text(
            "policy_version",
            payload.get("policy_version", DEFAULT_POLICY_VERSION),
        ),
    )
    validate_signal_bounds(signal)
    return signal


def validate_signal_bounds(signal: DemoSignal) -> None:
    for name in ("score", "uncertainty", "limit"):
        if getattr(signal, name) > SCORE_SCALE:
            raise ValueError(f"{name} exceeds SCORE_SCALE")

    if signal.warn_margin >= signal.limit:
        raise ValueError("warn_margin must be lower than limit")

    if signal.score + signal.uncertainty > 2 * SCORE_SCALE:
        raise ValueError("score plus uncertainty exceeds bounded demo range")


def derive_verdict(signal: DemoSignal) -> tuple[Verdict, str]:
    if not signal.metadata_complete:
        return "BLOCK", "Required metadata is incomplete."

    upper_bound = signal.score + signal.uncertainty
    safe_limit = signal.limit - signal.warn_margin

    if upper_bound <= safe_limit:
        return "PASS", "Score plus uncertainty is inside the safe envelope."

    if upper_bound <= signal.limit:
        return "WARN", "Score plus uncertainty requires review."

    return "BLOCK", "Score plus uncertainty exceeds the allowed envelope."


def build_evidence(signal: DemoSignal) -> DemoEvidence:
    verdict, reason = derive_verdict(signal)
    input_payload = asdict(signal)
    input_digest = sha256_tag(input_payload)
    evidence_material = {
        "input_digest": input_digest,
        "policy_id": signal.policy_id,
        "policy_version": signal.policy_version,
        "reason": reason,
        "schema_version": "aos-demo-evidence/v1",
        "signal_id": signal.signal_id,
        "verdict": verdict,
    }

    return DemoEvidence(
        schema_version="aos-demo-evidence/v1",
        signal_id=signal.signal_id,
        verdict=verdict,
        reason=reason,
        audit_id=sha256_tag(evidence_material),
        input_digest=input_digest,
        policy_id=signal.policy_id,
        policy_version=signal.policy_version,
        replayable=True,
        claim_boundary={
            "external_validation_claim": False,
            "production_use_claim": False,
            "regulated_use_claim": False,
        },
        input=input_payload,
    )


def verify_evidence(evidence_payload: dict[str, Any]) -> dict[str, Any]:
    if "input" not in evidence_payload:
        raise ValueError("evidence packet has no input field")

    input_payload = evidence_payload["input"]
    if not isinstance(input_payload, dict):
        raise ValueError("evidence input must be an object")

    replayed = asdict(build_evidence(parse_signal(input_payload)))
    checked_fields = (
        "schema_version",
        "signal_id",
        "verdict",
        "reason",
        "audit_id",
        "input_digest",
        "policy_id",
        "policy_version",
        "replayable",
        "claim_boundary",
    )
    mismatches = [
        {
            "field": field,
            "expected": replayed[field],
            "observed": evidence_payload.get(field),
        }
        for field in checked_fields
        if evidence_payload.get(field) != replayed[field]
    ]

    return {
        "valid": not mismatches,
        "mismatches": mismatches,
        "replayed": replayed,
    }


class AOSDemoGateHandler(BaseHTTPRequestHandler):
    server_version = "AOSDemoGate/0.1"

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self.write_json(200, {"status": "ok"})
            return
        self.write_json(404, {"error": "not_found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            payload = self.read_json()
            if path == "/v1/evaluate":
                self.write_json(200, asdict(build_evidence(parse_signal(payload))))
                return
            if path == "/v1/replay":
                self.write_json(200, verify_evidence(payload))
                return
            self.write_json(404, {"error": "not_found"})
        except ValueError as exc:
            self.write_json(400, {"error": "bad_request", "message": str(exc)})

    def read_json(self) -> dict[str, Any]:
        length_header = self.headers.get("Content-Length")
        if length_header is None:
            raise ValueError("missing Content-Length header")

        try:
            length = int(length_header)
        except ValueError as exc:
            raise ValueError("invalid Content-Length header") from exc

        if length < 0 or length > MAX_BODY_BYTES:
            raise ValueError("request body is outside the demo size limit")

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}") from exc

        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")

        return payload

    def write_json(self, status: int, payload: dict[str, Any]) -> None:
        body = canonical_json_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("[aos-demo-gate] " + fmt % args + "\n")


def load_json_file(path: str) -> dict[str, Any]:
    if path == "-":
        payload = json.load(sys.stdin)
    else:
        with open(path, encoding="utf-8") as file:
            payload = json.load(file)
    if not isinstance(payload, dict):
        raise ValueError("JSON file must contain an object")
    return payload


def write_json_file(path: str, payload: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True, ensure_ascii=False)
        file.write("\n")


def command_evaluate(args: argparse.Namespace) -> int:
    payload = asdict(build_evidence(parse_signal(load_json_file(args.input))))
    if args.output:
        write_json_file(args.output, payload)
    else:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_replay(args: argparse.Namespace) -> int:
    result = verify_evidence(load_json_file(args.evidence))
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["valid"] else 1


def command_serve(args: argparse.Namespace) -> int:
    server = HTTPServer((args.host, args.port), AOSDemoGateHandler)
    print(f"AOS demo gate API running on http://{args.host}:{args.port}")
    print("Endpoints: GET /health, POST /v1/evaluate, POST /v1/replay")
    server.serve_forever()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aos_api_gate.py",
        description="AOS public API-gate demo with replayable evidence.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate one input JSON file.")
    evaluate.add_argument("--input", required=True)
    evaluate.add_argument("--output")

    replay = subparsers.add_parser("replay", help="Replay one evidence JSON file.")
    replay.add_argument("--evidence", required=True, help="Path or '-' for stdin.")

    serve = subparsers.add_parser("serve", help="Run the local demo HTTP API.")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", default=8080, type=int)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "evaluate":
        return command_evaluate(args)
    if args.command == "replay":
        return command_replay(args)
    if args.command == "serve":
        return command_serve(args)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

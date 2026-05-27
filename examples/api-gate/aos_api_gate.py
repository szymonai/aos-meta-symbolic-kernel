from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

MAX_BODY_BYTES = 64 * 1024

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.aos_public_core import (  # noqa: E402
    build_signal_evidence,
    canonical_json_bytes,
    parse_signal,
    verify_signal_evidence,
)


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
                evidence = build_signal_evidence(parse_signal(payload))
                self.write_json(200, asdict(evidence))
                return
            if path == "/v1/replay":
                self.write_json(200, verify_signal_evidence(payload))
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
    evidence = build_signal_evidence(parse_signal(load_json_file(args.input)))
    payload = asdict(evidence)
    if args.output:
        write_json_file(args.output, payload)
    else:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


def command_replay(args: argparse.Namespace) -> int:
    result = verify_signal_evidence(load_json_file(args.evidence))
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

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "aos-frozen-public-output/v1"

CATEGORY_ALIASES = {
    "SUPPORTED": "SUPPORTED",
    "SUPPORT": "SUPPORTED",
    "SUPPORTS": "SUPPORTED",
    "INSUFFICIENT_EVIDENCE": "INSUFFICIENT_EVIDENCE",
    "NOT_ENOUGH_INFO": "INSUFFICIENT_EVIDENCE",
    "NOT ENOUGH INFO": "INSUFFICIENT_EVIDENCE",
    "NEI": "INSUFFICIENT_EVIDENCE",
    "UNSUPPORTED": "UNSUPPORTED",
    "REFUTES": "UNSUPPORTED",
    "REFUTED": "UNSUPPORTED",
    "HALLUCINATION": "UNSUPPORTED",
    "HALLUCINATED": "UNSUPPORTED",
    "POLICY_VIOLATION": "POLICY_VIOLATION",
    "UNSAFE_ACTION": "UNSAFE_ACTION",
}

EXPECTED_VERDICTS = {
    "SUPPORTED": "PASS",
    "INSUFFICIENT_EVIDENCE": "WARN",
    "UNSUPPORTED": "BLOCK",
    "POLICY_VIOLATION": "BLOCK",
    "UNSAFE_ACTION": "BLOCK",
}

DEFAULT_SIGNAL_FIELDS = {
    "policy_violation_count": "policy_violation_count",
    "provided_citation_count": "provided_citation_count",
    "required_citation_count": "required_citation_count",
    "source_coverage": "source_coverage",
    "unsafe_action_count": "unsafe_action_count",
    "unsupported_claim_count": "unsupported_claim_count",
}


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".jsonl":
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
    else:
        rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError("input must contain a JSON list or JSONL object stream")
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("all public-output rows must be JSON objects")
    return rows


def normalize_category(value: object) -> str:
    key = str(value).strip().upper()
    if key not in CATEGORY_ALIASES:
        raise ValueError(f"unsupported category label: {value!r}")
    return CATEGORY_ALIASES[key]


def require_field(row: dict[str, Any], field: str, row_index: int) -> Any:
    if field not in row:
        raise ValueError(f"row {row_index} is missing required field: {field}")
    return row[field]


def signal_value(
    row: dict[str, Any],
    row_index: int,
    output_field: str,
    *,
    as_float: bool = False,
) -> int | float:
    value = require_field(row, output_field, row_index)
    if as_float:
        return float(value)
    return int(value)


def build_frozen_record(
    row: dict[str, Any],
    row_index: int,
    *,
    source_dataset: str,
    source_split: str,
    model_id: str,
    id_field: str,
    output_field: str,
    category_field: str,
    difficulty_field: str,
    signal_fields: dict[str, str],
) -> dict[str, Any]:
    category = normalize_category(require_field(row, category_field, row_index))
    model_output = str(require_field(row, output_field, row_index))
    record = {
        "id": str(require_field(row, id_field, row_index)),
        "freeze_schema_version": SCHEMA_VERSION,
        "source_dataset": source_dataset,
        "source_split": source_split,
        "source_record_sha256": canonical_json_sha256(row),
        "model_id": model_id,
        "model_output": model_output,
        "model_output_sha256": text_sha256(model_output),
        "category": category,
        "difficulty_class": str(require_field(row, difficulty_field, row_index)),
        "expected_aos_verdict": EXPECTED_VERDICTS[category],
        "policy_violation_count": signal_value(
            row,
            row_index,
            signal_fields["policy_violation_count"],
        ),
        "provided_citation_count": signal_value(
            row,
            row_index,
            signal_fields["provided_citation_count"],
        ),
        "required_citation_count": signal_value(
            row,
            row_index,
            signal_fields["required_citation_count"],
        ),
        "source_coverage": signal_value(
            row,
            row_index,
            signal_fields["source_coverage"],
            as_float=True,
        ),
        "unsafe_action_count": signal_value(
            row,
            row_index,
            signal_fields["unsafe_action_count"],
        ),
        "unsupported_claim_count": signal_value(
            row,
            row_index,
            signal_fields["unsupported_claim_count"],
        ),
    }
    for optional_field in ("prompt", "reference_evidence", "policy"):
        if optional_field in row:
            record[optional_field] = row[optional_field]
    return record


def freeze_rows(
    rows: list[dict[str, Any]],
    *,
    source_dataset: str,
    source_split: str,
    model_id: str,
    id_field: str = "id",
    output_field: str = "model_output",
    category_field: str = "category",
    difficulty_field: str = "difficulty_class",
    signal_fields: dict[str, str] | None = None,
    max_records: int | None = None,
) -> list[dict[str, Any]]:
    active_signal_fields = signal_fields or DEFAULT_SIGNAL_FIELDS
    selected_rows = rows[:max_records] if max_records is not None else rows
    return [
        build_frozen_record(
            row,
            index,
            source_dataset=source_dataset,
            source_split=source_split,
            model_id=model_id,
            id_field=id_field,
            output_field=output_field,
            category_field=category_field,
            difficulty_field=difficulty_field,
            signal_fields=active_signal_fields,
        )
        for index, row in enumerate(selected_rows)
    ]


def records_to_jsonl(records: list[dict[str, Any]]) -> str:
    return "\n".join(
        json.dumps(record, allow_nan=False, separators=(",", ":"), sort_keys=True)
        for record in records
    ) + "\n"


def run(
    *,
    input_path: Path,
    output_path: Path,
    source_dataset: str,
    source_split: str,
    model_id: str,
    id_field: str = "id",
    output_field: str = "model_output",
    category_field: str = "category",
    difficulty_field: str = "difficulty_class",
    signal_fields: dict[str, str] | None = None,
    max_records: int | None = None,
    write: bool = True,
) -> list[dict[str, Any]]:
    rows = load_rows(input_path)
    records = freeze_rows(
        rows,
        source_dataset=source_dataset,
        source_split=source_split,
        model_id=model_id,
        id_field=id_field,
        output_field=output_field,
        category_field=category_field,
        difficulty_field=difficulty_field,
        signal_fields=signal_fields,
        max_records=max_records,
    )
    if write:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(records_to_jsonl(records), encoding="utf-8")
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-dataset", required=True)
    parser.add_argument("--source-split", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--id-field", default="id")
    parser.add_argument("--output-field", default="model_output")
    parser.add_argument("--category-field", default="category")
    parser.add_argument("--difficulty-field", default="difficulty_class")
    parser.add_argument("--max-records", type=int)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    records = run(
        input_path=args.input,
        output_path=args.output,
        source_dataset=args.source_dataset,
        source_split=args.source_split,
        model_id=args.model_id,
        id_field=args.id_field,
        output_field=args.output_field,
        category_field=args.category_field,
        difficulty_field=args.difficulty_field,
        max_records=args.max_records,
        write=not args.check,
    )
    if args.check and args.output.read_text(encoding="utf-8") != records_to_jsonl(
        records
    ):
        raise SystemExit(f"{args.output} is not up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

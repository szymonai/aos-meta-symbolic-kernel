from __future__ import annotations

import pytest

from core.aos_public_core import derive_verdict

VERDICT_RANK = {"PASS": 0, "WARN": 1, "BLOCK": 2}


def abstract_interval_verdict(
    upper_bound: int,
    limit: int,
    warn_margin: int,
) -> str:
    if upper_bound > limit:
        return "BLOCK"
    if upper_bound > limit - warn_margin:
        return "WARN"
    return "PASS"


@pytest.mark.parametrize("limit", [-10, 0, 25, 100])
@pytest.mark.parametrize("warn_margin", [0, 1, 5, 20])
def test_python_verdict_matches_abstract_integer_model(
    limit: int,
    warn_margin: int,
) -> None:
    for upper_bound in range(limit - warn_margin - 3, limit + 4):
        assert derive_verdict(
            float(upper_bound),
            float(limit),
            float(warn_margin),
        ) == abstract_interval_verdict(upper_bound, limit, warn_margin)


@pytest.mark.parametrize("limit", [-10, 0, 25, 100])
@pytest.mark.parametrize("warn_margin", [0, 1, 5, 20])
def test_python_verdict_is_monotone_on_integer_like_subset(
    limit: int,
    warn_margin: int,
) -> None:
    upper_bounds = list(range(limit - warn_margin - 5, limit + 6))
    verdicts = [
        derive_verdict(float(upper_bound), float(limit), float(warn_margin))
        for upper_bound in upper_bounds
    ]

    for earlier, later in zip(verdicts, verdicts[1:]):
        assert VERDICT_RANK[earlier] <= VERDICT_RANK[later]

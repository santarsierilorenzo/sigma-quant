from __future__ import annotations

from .typing import Frequency


_PERIODS_PER_YEAR: dict[Frequency, int] = {
    "D": 252,
    "W": 52,
    "M": 12,
    "Y": 1,
}

_PANDAS_RULE: dict[Frequency, str] = {
    "D": "D",
    "W": "W",
    "M": "ME",
    "Y": "YE",
}


def periods_per_year(frequency: Frequency) -> int:
    """
    Return the number of periods per year implied by a frequency.
    """
    try:
        return _PERIODS_PER_YEAR[frequency]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported frequency: {frequency}"
        ) from exc


def pandas_rule(frequency: Frequency) -> str:
    """
    Return the pandas resampling rule for a given frequency.
    """
    try:
        return _PANDAS_RULE[frequency]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported frequency: {frequency}"
        ) from exc

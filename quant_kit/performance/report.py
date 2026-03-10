from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, Literal

import numpy as np
import pandas as pd

from ..custom_typing import ArrayLike, Frequency
from ..utils import periods_per_year
from .metrics import (
    calmar_ratio,
    excess_kurtosis,
    hit_rate,
    information_ratio,
    omega_ratio,
    sharpe_ratio,
    skew,
    sortino_ratio,
    tracking_error,
)
from .returns import annual_return, cum_returns
from .risk import (
    annual_vola,
    drawdown_stats,
    downside_risk,
    max_drawdown,
    tail_ratio,
    upside_risk,
)


def ascii_report(
    returns: ArrayLike,
    frequency: Frequency,
    *,
    strategy_name: str = "Portfolio",
    benchmark_returns: Iterable[float] | None = None,
    kind: Literal["simple", "log", "pnl"] = "simple",
    starting_value: float = 0.0,
    risk_free: float = 0.0,
    mar: float = 0.0,
    required_return: float = 0.0,
    as_of: str | date | datetime | None = None,
    width: int = 66,
) -> str:
    """
    Build an ASCII performance report using metrics from
    ``quant_kit.performance``.

    Parameters
    ----------
    returns
        Strategy return or PnL series.
    frequency
        Sampling frequency of the input series.
    strategy_name
        Label shown in the report header.
    benchmark_returns
        Optional benchmark or factor return series. When provided, tracking
        error and information ratio are included.
    kind
        Input series type.
    starting_value
        Starting value passed to cumulative/drawdown computations.
    risk_free
        Per-period risk-free rate used for the Sharpe ratio.
    mar
        Minimum acceptable return used for the Sortino ratio.
    required_return
        Annual required return used for the Omega ratio.
    as_of
        Report date shown in the header. If omitted and ``returns`` is a
        pandas Series with a datetime index, the last timestamp is used.
    width
        Total line width for the rendered report.

    Returns
    -------
    str
        Formatted ASCII report.
    """
    values = _to_numpy(returns)

    if values.size == 0:
        raise ValueError("`returns` must contain at least one observation.")

    benchmark = (
        None if benchmark_returns is None
        else _to_numpy(benchmark_returns)
    )

    annualization = periods_per_year(frequency)
    header_date = _resolve_as_of(returns, as_of)
    dd_stats = drawdown_stats(
        returns,
        kind=kind,
        starting_value=starting_value,
    )

    sections: list[tuple[str, list[tuple[str, str]]]] = [
        (
            "RETURN METRICS",
            [
                (
                    "Total Return",
                    _format_percent(
                        _total_return(
                            returns,
                            kind,
                            starting_value,
                        )
                    ),
                ),
                (
                    "Annualized Return",
                    _format_percent(
                        annual_return(
                            returns,
                            frequency,
                            kind=kind,
                        )
                    ),
                ),
            ],
        ),
        (
            "RISK METRICS",
            [
                (
                    "Annualized Volatility",
                    _format_percent(
                        annual_vola(values, frequency)
                    ),
                ),
                ("Downside Risk", _format_percent(downside_risk(values))),
                ("Upside Risk", _format_percent(upside_risk(values))),
                ("Skewness", _format_float(skew(values))),
                ("Excess Kurtosis", _format_float(excess_kurtosis(values))),
            ],
        ),
        (
            "RISK-ADJUSTED PERFORMANCE",
            [
                (
                    "Sharpe Ratio",
                    _format_float(
                        sharpe_ratio(
                            values,
                            frequency,
                            risk_free=risk_free,
                        )
                    ),
                ),
                (
                    "Sortino Ratio",
                    _format_float(
                        sortino_ratio(
                            values,
                            frequency,
                            mar=mar,
                        )
                    ),
                ),
                (
                    "Calmar Ratio",
                    _format_float(
                        calmar_ratio(
                            values,
                            frequency,
                            kind=kind,
                        )
                    ),
                ),
                (
                    "Omega Ratio",
                    _format_float(
                        omega_ratio(
                            values,
                            required_return,
                            frequency,
                        )
                    ),
                ),
            ],
        ),
        (
            "DRAWDOWN ANALYSIS",
            [
                (
                    "Maximum Drawdown",
                    _format_percent(
                        max_drawdown(
                            returns,
                            kind=kind,
                            starting_value=starting_value,
                        )
                    ),
                ),
                (
                    "Average Drawdown",
                    _format_percent(dd_stats["Avg Drawdown"]),
                ),
                (
                    "Max Time Underwater",
                    _format_days(dd_stats["Max Time Underwater"]),
                ),
                (
                    "Avg Time Underwater",
                    _format_days(dd_stats["Avg Time Underwater"]),
                ),
            ],
        ),
        (
            "DISTRIBUTION",
            [
                ("Hit Rate", _format_percent(hit_rate(values))),
                ("Tail Ratio", _format_float(tail_ratio(values))),
            ],
        ),
    ]

    if benchmark is not None:
        sections[2][1].extend(
            [
                (
                    "Tracking Error",
                    _format_float(
                        tracking_error(values, benchmark)
                    ),
                ),
                (
                    "Information Ratio",
                    _format_float(
                        information_ratio(values, benchmark)
                    ),
                ),
            ]
        )

    lines = [
        "=" * width,
        "PORTFOLIO PERFORMANCE REPORT".center(width),
        "=" * width,
        (
            f"Strategy: {strategy_name} | "
            f"Sample size: {values.size} | Date: {header_date}"
        ),
        f"Annualization: {annualization} periods per year",
        "",
    ]

    for title, metrics in sections:
        lines.append(title)
        lines.append("-" * width)
        lines.extend(
            _format_metric_row(label, value, width)
            for label, value in metrics
        )
        lines.append("")

    return "\n".join(lines).rstrip()


def _to_numpy(values: ArrayLike) -> np.ndarray:
    source = (
        list(values)
        if not isinstance(values, np.ndarray)
        else values
    )
    arr = np.asarray(source, dtype=float)
    return arr[~np.isnan(arr)]


def _resolve_as_of(
    returns: ArrayLike,
    as_of: str | date | datetime | None,
) -> str:
    if as_of is not None:
        if isinstance(as_of, (date, datetime)):
            return as_of.strftime("%Y-%m-%d")
        return str(as_of)

    if (
        isinstance(returns, pd.Series)
        and isinstance(returns.index, pd.DatetimeIndex)
        and len(returns.index) > 0
    ):
        return returns.index[-1].strftime("%Y-%m-%d")

    return "N/A"


def _total_return(
    returns: ArrayLike,
    kind: Literal["simple", "log", "pnl"],
    starting_value: float,
) -> float:
    cumulative = cum_returns(returns, kind=kind, starting_value=starting_value)
    return float(np.asarray(cumulative, dtype=float)[-1])


def _format_metric_row(label: str, value: str, width: int) -> str:
    dots = max(width - len(label) - len(value), 2)
    return f"{label}{' ' * dots}{value}"


def _format_percent(value: float) -> str:
    if np.isnan(value):
        return "n/a"
    return f"{value * 100:,.2f} %"


def _format_float(value: float) -> str:
    if np.isnan(value):
        return "n/a"
    return f"{value:,.2f}"


def _format_days(value: float | int) -> str:
    if np.isnan(value):
        return "n/a"
    if float(value).is_integer():
        return f"{int(value)} periods"
    return f"{value:.2f} periods"

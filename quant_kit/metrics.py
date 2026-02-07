from __future__ import annotations

from .risk import downside_risk, drawdown
from .typing import ArrayLike, Frequency
from .utils import periods_per_year
from typing import Iterable
import pandas as pd
import numpy as np


def sharpe_ratio(
    returns: Iterable[float],
    frequency: Frequency,
    annualize: bool = True,
    risk_free: float = 0.0,
) -> float:
    """
    Compute the Sharpe ratio.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size < 2:
        return np.nan

    mean = arr.mean() - risk_free
    std = arr.std(ddof=1)

    if std == 0.0:
        return np.nan

    scale = (
        np.sqrt(periods_per_year(frequency))
        if annualize
        else 1.0
    )
    return mean / std * scale


def sortino_ratio(
    returns: Iterable[float],
    frequency: Frequency,
    annualize: bool = True,
    mar: float = 0.0,
) -> float:
    """
    Compute the Sortino ratio.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size < 2:
        return np.nan

    mean_excess = arr.mean() - mar
    dsr = downside_risk(arr, mar)

    if dsr == 0.0:
        return np.nan

    scale = (
        np.sqrt(periods_per_year(frequency))
        if annualize
        else 1.0
    )
    return mean_excess / dsr * scale


def calmar_ratio(
    returns: ArrayLike,
    frequency: Frequency,
    kind: str = "simple",
) -> float:
    """
    Compute the Calmar ratio.
    """
    max_dd = abs(np.min(drawdown(returns, kind=kind)))
    if max_dd == 0:
        return np.nan

    n_years = len(list(returns)) / periods_per_year(frequency)
    if n_years <= 0:
        return np.nan

    total = np.sum(returns)
    return (total / n_years) / max_dd


def omega_ratio(
    returns: Iterable[float],
    required_return: float,
    frequency: Frequency,
) -> float:
    """
    Compute the Omega ratio.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size < 2:
        return np.nan

    if required_return <= -1.0:
        return np.nan

    periods = periods_per_year(frequency)

    if periods == 1:
        threshold = required_return
    else:
        threshold = (1.0 + required_return) ** (
            1.0 / periods
        ) - 1.0

    excess = arr - threshold

    gains = np.sum(np.maximum(excess, 0.0))
    losses = np.sum(np.maximum(-excess, 0.0))

    if losses == 0.0:
        return np.nan

    return gains / losses


def hit_rate(
    returns: Iterable[float],
) -> float:
    """
    Fraction of strictly positive observations.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size == 0:
        return np.nan

    return float(np.mean(arr > 0.0))


def period_hit_rate(
    returns: pd.Series,
    frequency: Frequency,
) -> pd.Series:
    """
    Compute the hit ratio on aggregated periods.

    The function aggregates returns at the specified frequency and
    computes the hit ratio for each aggregated period. A period is
    considered a "hit" if the aggregated return is strictly positive.

    Parameters
    ----------
    returns
        Time series of periodic returns indexed by datetime.
    frequency
        Aggregation frequency:
        - "D": daily
        - "W": weekly
        - "M": monthly
        - "Y": yearly

    Returns
    -------
    pandas.Series
        Time series of hit ratios computed on aggregated periods.
        Each value represents the fraction of positive observations
        within the corresponding period.
    """
    if not isinstance(returns, pd.Series):
        raise TypeError("`returns` must be a pandas Series.")

    rule = _PANDAS_RULE.get(frequency)
    if rule is None:
        raise ValueError(f"Unsupported frequency: {frequency}")

    return returns.resample(rule).apply(hit_rate)


def skew(
    returns: Iterable[float],
) -> float:
    """
    Compute skewness.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    mu = arr.mean()
    sigma = arr.std(ddof=1)

    return np.mean(((arr - mu) / sigma) ** 3)


def excess_kurtosis(
    returns: Iterable[float],
) -> float:
    """
    Compute excess kurtosis.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    mu = arr.mean()
    sigma = arr.std(ddof=1)

    return np.mean(((arr - mu) / sigma) ** 4) - 3.0


def tracking_error(
    returns: Iterable[float],
    factor_returns: Iterable[float],
) -> float:
    """
    Compute tracking error as the sample standard deviation
    of active returns.

    Parameters
    ----------
    returns : Iterable[float]
        Time series of portfolio returns.
    factor_returns : Iterable[float]
        Time series of factor or benchmark returns. Must be aligned
        in time with `returns`.

    Returns
    -------
    float
        Sample standard deviation of active returns (ddof=1).
    """
    ar = active_return(returns, factor_returns)
    return float(np.nanstd(ar, ddof=1))


def information_ratio(
    returns: Iterable[float],
    factor_returns: Iterable[float],
) -> float:
    """
    Compute the Information Ratio.

    The Information Ratio measures the risk-adjusted performance of a
    strategy relative to a benchmark or factor. It is defined as the
    ratio between the average active return and the tracking error.

    Parameters
    ----------
    returns
        Sequence of strategy returns.
    factor_returns
        Sequence of benchmark or factor returns. Must be aligned with
        `returns`.

    Returns
    -------
    float
        Information Ratio.

    Notes
    -----
    The Information Ratio is defined as:

        IR = mean(r_t - b_t) / std(r_t - b_t)

    where r_t are the strategy returns and b_t are the benchmark or
    factor returns.

    The function assumes that `active_return` returns the mean active
    return and that `tracking_error` returns the standard deviation of
    active returns.

    If the tracking error is zero or undefined, the Information Ratio
    is undefined and NaN is returned.
    """
    returns_arr = np.asarray(list(returns), dtype=float)
    factor_arr = np.asarray(list(factor_returns), dtype=float)

    mask = ~np.isnan(returns_arr) & ~np.isnan(factor_arr)
    returns_arr = returns_arr[mask]
    factor_arr = factor_arr[mask]

    if returns_arr.size < 2:
        return np.nan

    ar = active_return(returns_arr, factor_arr)
    te = tracking_error(returns_arr, factor_arr)

    if te == 0.0 or np.isnan(te):
        return np.nan

    return ar / te

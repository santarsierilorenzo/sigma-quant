from __future__ import annotations

from .risk import downside_risk, drawdown
from .typing import ArrayLike, Frequency
from .utils import periods_per_year
from .returns import _active_return
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
    Compute the Sharpe ratio for a series of periodic returns.
    If annualize is True, the Sharpe ratio is annualized by multiplying the
    non-annualized estimate by the square root of the number of periods per
    year implied by frequency.

    Parameters
    ----------
    returns
        Sequence of periodic returns.
    frequency
        Frequency of the returns:
        - "D": `daily`
        - "W": `weekly`
        - "M": `monthly`
        - "Y": `yearly`
    annualize
        If True, the Sharpe ratio is scaled to annual frequency.
    risk_free
        Risk-free rate per period (same frequency as `returns`).

    Returns
    -------
    float
        Sharpe ratio.

    Notes
    -----
    Notes
    -----
    - NaN values ignored.

    - Formula:
    .. math::

        \text{Sharpe} =
        \frac{\overline{R_p - R_f}}{\operatorname{std}(R_p - R_f)}

    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]
    arr -= risk_free

    if arr.size < 2:
        return np.nan

    mean = arr.mean()
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

    The Sortino ratio measures the excess return relative to a minimum
    acceptable return (MAR), adjusted for downside risk only.

    Parameters
    ----------
    returns
        Sequence of periodic returns.
    frequency
        Frequency of the returns:
        - "D": daily
        - "W": weekly
        - "M": monthly
        - "Y": yearly
    annualize
        If True, the Sortino ratio is scaled to annual frequency.
    risk_free
        Risk-free rate per period. This parameter is ignored unless
        explicitly used as MAR.
    mar
        Minimum acceptable return. This value is used consistently
        both in the numerator and in the downside risk computation.

    Returns
    -------
    float
        Sortino ratio.

    Notes
    -----
    The Sortino ratio is defined as:

        Sortino = E[r_t - MAR] / sqrt( E[min(r_t - MAR, 0)^2] )

    where r_t are the periodic returns.

    NaN values are ignored. The result is annualized using the
    square-root-of-time rule when `annualize=True`.
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
    Compute the Calmar ratio or a Calmar-like metric.
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

    The Omega ratio measures the probability-weighted gains relative
    to probability-weighted losses with respect to a required return.

    The required return is expressed at annual frequency and is
    internally converted to the same frequency as the input returns.

    Parameters
    ----------
    returns
        Sequence of periodic returns.
    required_return
        Annual required (minimum acceptable) return.
    frequency
        Frequency of the input returns:
        - "D": daily
        - "W": weekly
        - "M": monthly
        - "Y": yearly

    Returns
    -------
    float
        Omega ratio.

    Notes
    -----
    The Omega ratio is defined as:

        Omega(tau) =
            sum( max(r_t - tau, 0) ) /
            sum( max(tau - r_t, 0) )

    where r_t are the periodic returns and tau is the required return
    converted to the same frequency as `returns`.

    The annual required return is converted as:

        tau = (1 + required_return) ** (1 / N) - 1

    where N is the number of periods per year implied by `frequency`.

    NaN values are ignored. If no downside deviations are present,
    the Omega ratio is undefined and NaN is returned.
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
    Compute the hit ratio.

    The hit ratio is defined as the fraction of periods with strictly
    positive returns.

    Parameters
    ----------
    returns
        Sequence of periodic returns or PnL values.

    Returns
    -------
    float
        Hit ratio, i.e. the proportion of observations where the
        return (or PnL) is greater than zero.

    Notes
    -----
    NaN values are ignored.

    A hit ratio close to 0.5 indicates that positive and negative
    outcomes occur with similar frequency, while higher values
    indicate a larger proportion of positive periods.

    This metric does not take into account the magnitude of returns,
    only their sign.
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
    Compute the skewness of a return series.

    Skewness measures the asymmetry of a distribution around its mean.
    Positive skewness indicates a longer or fatter right tail, while
    negative skewness indicates a longer or fatter left tail.

    Parameters
    ----------
    returns
        Sequence of periodic returns or PnL values.

    Returns
    -------
    float
        Skewness of the input series.

    Notes
    -----
    Skewness is defined as:

        E[ ((X - mu) / sigma)^3 ]

    where mu is the sample mean and sigma is the sample standard
    deviation computed with ddof=1.

    NaN values are ignored. The estimator does not apply a finite-sample
    bias correction.
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
    Compute the excess kurtosis of a return series.

    Excess kurtosis measures the degree of tail heaviness of a
    distribution relative to a normal distribution. A normal
    distribution has zero excess kurtosis.

    Parameters
    ----------
    returns
        Sequence of periodic returns or PnL values.

    Returns
    -------
    float
        Excess kurtosis of the input series.

    Notes
    -----
    Excess kurtosis is defined as:

        E[ ((X - mu) / sigma)^4 ] - 3

    where mu is the sample mean and sigma is the sample standard
    deviation computed with ddof=1.

    NaN values are ignored. The estimator does not apply a finite-sample
    bias correction.
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
    ar = _active_return(returns, factor_returns)
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

    The function assumes that `_active_return` returns the mean active
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

    ar = _active_return(returns_arr, factor_arr)
    te = tracking_error(returns_arr, factor_arr)

    if te == 0.0 or np.isnan(te):
        return np.nan

    return ar / te

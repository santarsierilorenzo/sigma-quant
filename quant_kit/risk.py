from __future__ import annotations

from .typing import ArrayLike, Frequency
from .utils import periods_per_year
from .returns import cum_returns
from typing import Literal
import pandas as pd
import numpy as np


def drawdown(
    returns: ArrayLike,
    kind: Literal["simple", "pnl", "log"] = "simple",
    starting_value: float = 0.0,
):
    """
    Compute the drawdown series.

    The drawdown is computed from the equity curve implied by the
    input returns or PnL.

    Parameters
    ----------
    returns
        Input time series:
        - kind="simple": simple returns
        - kind="log": log-returns
        - kind="pnl": additive PnL
    kind
        Type of input values.
    starting_value
        Initial cumulative level. For PnL inputs, this represents
        the initial capital.

    Returns
    -------
    pandas.Series or numpy.ndarray
        Drawdown series:
        - relative drawdown for simple and log returns
        - relative drawdown for pnl if starting_value > 0
        - absolute drawdown for pnl if starting_value == 0

    Notes
    -----
    Relative drawdown is defined as:

        DD_t = W_t / max_{s <= t} W_s - 1

    where W_t is the equity curve.
    """
    cumulative = cum_returns(
        returns,
        kind=kind,
        starting_value=starting_value,
    )

    if kind == "simple":
        equity = 1.0 + cumulative
    elif kind == "log":
        equity = np.exp(cumulative)
    else:
        equity = cumulative

    running_max = np.maximum.accumulate(equity)

    if kind == "pnl" and starting_value == 0.0:
        # Absolute drawdown in monetary units
        return equity - running_max

    return equity / running_max - 1.0


def max_drawdown(
    returns: ArrayLike,
    kind: Literal["simple", "pnl", "log"] = "simple",
    starting_value: float = 0.0,
) -> float:
    """
    Compute the maximum drawdown.

    The maximum drawdown is defined as the minimum value of the
    drawdown series over the full sample.

    Parameters
    ----------
    returns
        Input time series.
    kind
        Type of input values.
    starting_value
        Initial cumulative level.

    Returns
    -------
    float
        Maximum drawdown (non-positive).
    """
    dd = drawdown(
        returns,
        kind=kind,
        starting_value=starting_value,
    )
    return float(np.min(dd))


def annual_vola(
    returns: ArrayLike,
    frequency: Frequency,
) -> float:
    """
    Compute annualized volatility.

    The function computes the sample standard deviation of periodic
    returns and scales it to annual frequency using the square-root-
    of-time rule.

    Parameters
    ----------
    returns
        Time series of periodic returns.
    frequency
        Frequency of the input data.

    Returns
    -------
    float
        Annualized volatility.

    Notes
    -----
    NaN values are ignored. If fewer than two valid observations
    are available, NaN is returned.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size < 2:
        return np.nan

    return float(
        np.std(arr, ddof=1)
        * np.sqrt(periods_per_year(frequency))
    )


def downside_risk(
    returns: ArrayLike,
    m: float = 0.0,
) -> float:
    """
    Compute downside risk (semi-deviation).

    Downside risk is defined as the square root of the mean squared
    negative deviations of returns below a threshold level `m`.

    Parameters
    ----------
    returns
        Time series of periodic returns.
    m
        Threshold return. Only deviations below this level contribute
        to the downside risk.

    Returns
    -------
    float
        Downside risk (semi-deviation).

    Notes
    -----
    Downside risk is computed as:

        sqrt( mean( min(r_t - m, 0)^2 ) )

    NaN values are ignored.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size == 0:
        return np.nan

    downside = np.minimum(arr - m, 0.0)
    return float(np.sqrt(np.mean(downside ** 2)))


def upside_risk(
    returns: ArrayLike,
    m: float = 0.0,
) -> float:
    """
    Compute upside risk (upside semi-deviation).

    Upside risk is defined as the square root of the mean squared
    positive deviations of returns above a threshold level `m`.

    Parameters
    ----------
    returns
        Time series of periodic returns.
    m
        Threshold return. Only deviations above this level contribute
        to the upside risk.

    Returns
    -------
    float
        Upside risk (upside semi-deviation).

    Notes
    -----
    Upside risk is computed as:

        sqrt( mean( max(r_t - m, 0)^2 ) )

    NaN values are ignored.
    """
    arr = np.asarray(list(returns), dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size == 0:
        return np.nan

    upside = np.maximum(arr - m, 0.0)
    return float(np.sqrt(np.mean(upside ** 2)))


def time_underwater(
    drawdown: pd.Series,
) -> pd.Series:
    """
    Count consecutive underwater periods.

    An underwater period is defined as a period where the drawdown
    is strictly negative.

    Parameters
    ----------
    drawdown
        Drawdown time series.

    Returns
    -------
    pandas.Series
        Time series of consecutive underwater counts. The value is
        zero when the system is not underwater and increases
        sequentially during each underwater spell.
    """
    underwater = drawdown < 0.0

    c = np.cumsum(underwater.astype(int))
    reset = np.maximum.accumulate(
        np.where(~underwater, c, 0)
    )

    return pd.Series(c - reset, index=drawdown.index)


def drawdown_stats(
    returns: ArrayLike,
    kind: Literal["simple", "pnl", "log"] = "simple",
    starting_value: float = 0.0,
) -> dict:
    """
    Compute summary statistics for drawdowns.

    Parameters
    ----------
    returns
        Input time series.
    kind
        Type of input values.
    starting_value
        Initial cumulative level.

    Returns
    -------
    dict
        Dictionary containing drawdown magnitude and time-underwater
        statistics.
    """
    dd_series = drawdown(
        returns,
        kind=kind,
        starting_value=starting_value,
    )

    if not isinstance(dd_series, pd.Series):
        dd_series = pd.Series(dd_series)

    uw = time_underwater(dd_series).to_numpy()

    ends = np.where((uw[:-1] > 0) & (uw[1:] == 0))[0]
    spell_lengths = uw[ends]

    if uw[-1] > 0:
        spell_lengths = np.append(spell_lengths, uw[-1])

    dd_neg = dd_series[dd_series < 0.0]

    return {
        "Max Time Underwater": int(uw.max()),
        "Avg Time Underwater": float(
            np.round(spell_lengths.mean(), 2)
            if spell_lengths.size > 0 else 0.0
        ),
        "Max Drawdown": float(np.round(dd_neg.min(), 2)),
        "Avg Drawdown": float(np.round(dd_neg.mean(), 2)),
        "Drawdown Q1": float(np.round(np.quantile(dd_neg, 0.25), 2)),
        "Drawdown Q2": float(np.round(np.quantile(dd_neg, 0.50), 2)),
        "Drawdown Q3": float(np.round(np.quantile(dd_neg, 0.75), 2)),
    }

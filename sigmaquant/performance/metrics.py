from __future__ import annotations

from ..utils import periods_per_year, _PANDAS_RULE
from ..custom_typing import ArrayLike, Frequency
from .returns import _active_return, annual_return
from .risk import downside_risk, max_drawdown
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

    If ``annualize`` is True, the Sharpe ratio is annualized by multiplying the
    non-annualized estimate by the square root of the number of periods per
    year implied by ``frequency``.

    Parameters
    ----------
    returns : iterable of float
        Sequence of periodic portfolio returns.
    frequency
        Frequency of the returns:
            - ``"D"``: daily
            - ``"W"``: weekly
            - ``"M"``: monthly
            - ``"Y"``: yearly
    annualize : bool
        If True, the Sharpe ratio is scaled to annual frequency.
    risk_free : float
        Risk-free rate per period, expressed at the same frequency as
        ``returns``.

    Returns
    -------
    float
        Estimated Sharpe ratio.

    Notes
    -----
    - Missing values (NaN) are excluded from the computation.

    Let :math:`r_t` denote the periodic portfolio returns and
    :math:`r_f` the per-period risk-free rate.

    Define the sample mean excess return as:

    .. math::

        \\bar{r}_e =
        \\frac{1}{T}
        \\sum_{t=1}^{T}
        (r_t - r_f)

    and the sample standard deviation of excess returns as:

    .. math::

        s_e =
        \\sqrt{
            \\frac{1}{T - 1}
            \\sum_{t=1}^{T}
            \\left(
                (r_t - r_f) - \\bar{r}_e
            \\right)^2
        }

    The (non-annualized) Sharpe ratio estimator is:

    .. math::

        \\widehat{\\text{Sharpe}} =
        \\frac{\\bar{r}_e}{s_e}

    If ``annualize=True``, the estimator is scaled as:

    .. math::

        \\widehat{\\text{Sharpe}}_{ann} =
        \\sqrt{N}
        \\frac{\\bar{r}_e}{s_e}

    where :math:`N` is the number of periods per year implied by
    ``frequency``. 
    """
    arr = np.asarray(returns, dtype=float)
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

    mar
        Minimum acceptable return. This value is used consistently
        both in the numerator and in the downside risk computation.

    Returns
    -------
    float
        Sortino ratio.

    Notes
    -----
    - Missing values (NaN) are excluded from the computation.

    - The result is annualized using the square-root-of-time rule when
      `annualize=True`.

    - Risk-free rate is ignored unless explicitly used as MAR.

    Let :math:`r_t` denote the periodic returns and :math:`MAR`
    the minimum acceptable return.

    Define the sample mean excess return as:

    .. math::

        \\bar{r}_{MAR} =
        \\frac{1}{T}
        \\sum_{t=1}^{T}
        (r_t - MAR)

    Define the downside deviation as:

    .. math::

        s_d =
        \\sqrt{
            \\frac{1}{T - 1}
            \\sum_{t=1}^{T}
            \\min(r_t - MAR, 0)^2
        }

    The Sortino ratio estimator is:

    .. math::

        \\widehat{\\text{Sortino}} =
        \\frac{\\bar{r}_{MAR}}{s_d}

    If ``annualize=True``:

    .. math::

        \\widehat{\\text{Sortino}}_{ann} =
        \\sqrt{N}
        \\frac{\\bar{r}_{MAR}}{s_d}

    where :math:`N` is the number of periods per year.  
    """
    arr = np.asarray(returns, dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size < 2:
        return np.nan

    mean_excess = arr.mean() - mar
    dsr = downside_risk(arr, frequency, mar)

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

    Parameters
    ----------
    returns : ArrayLike
        Input time series:

        - ``kind="simple"``: simple returns
        - ``kind="log"``: log-returns
        - ``kind="pnl"``: additive PnL

    frequency : Frequency
        Sampling frequency of the input series:

        - ``"D"``: daily
        - ``"W"``: weekly
        - ``"M"``: monthly
        - ``"Y"``: yearly

    kind : str, default="simple"
        Type of input values.

    Returns
    -------
    float
        Calmar ratio.

    Notes
    -----
    The Calmar ratio is defined as:

    .. math::

        \\text{Calmar} =
        \\frac{\\mathrm{CAGR}}{\\left| \\mathrm{Max Drawdown} \\right|}

    where:

    - :math:`\\mathrm{CAGR}` is the compound annual growth rate.
    - :math:`\\mathrm{Max Drawdown}` is the maximum peak-to-trough drawdown
      over the sample period.

    If ``kind="pnl"``, a Calmar-like metric is computed:

    .. math::

        \\frac{\\text{Average Annual Return}}
        {\\left| \\text{Monetary Max Drawdown} \\right|}

    In this case the numerator is the annualized mean PnL and the
    denominator is the absolute monetary maximum drawdown.
    """
    max_dd = max_drawdown(
        returns,
        kind=kind,
    )

    if max_dd == 0:
        return np.nan

    ann_ret = annual_return(returns, frequency=frequency, kind=kind)
    
    return ann_ret / np.abs(max_dd)


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

    .. math::

        \\Omega(\\tau) =
        \\frac{
            \\sum_{t=1}^T \\max(r_t - \\tau, 0)
        }{
            \\sum_{t=1}^T \\max(\\tau - r_t, 0)
        }

    where :math:`r_t` are the periodic returns and :math:`\\tau` is the
    required return expressed at the same frequency as the input series.

    The annual required return :math:`R_{\\text{req}}` is converted to
    periodic frequency as:

    .. math::

        \\tau =
        \\begin{cases}
            R_{\\text{req}}, & N = 1 \\\\
            (1 + R_{\\text{req}})^{1 / N} - 1, & N > 1
        \\end{cases}

    where :math:`N` is the number of periods per year implied by
    ``frequency``.

    NaN values are ignored. If the denominator is zero (no downside
    deviations), the Omega ratio is undefined.
    """
    arr = np.asarray(returns, dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size < 2:
        return np.nan

    if required_return < 0:
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
    Compute the hit rate.

    The hit rate is defined as the fraction of periods with strictly
    positive returns.

    Parameters
    ----------
    returns
        Sequence of periodic returns or PnL values.

    Returns
    -------
    float
        Hit rate, i.e. the proportion of observations where the
        return (or PnL) is greater than zero.

    Notes
    -----
    The hit rate is defined as:

    .. math::

        \\text{Hit Rate} =
        \\frac{1}{T}
        \\sum_{t=1}^T
        \\mathbb{I}(r_t > 0)

    where :math:`\\mathbb{I}(\\cdot)` is the indicator function and
    :math:`r_t` are the periodic returns or PnL values.

    NaN values are ignored.
    """
    arr = np.asarray(returns, dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size == 0:
        return np.nan

    return float(np.mean(arr > 0))


def period_hit_rate(
    returns: pd.Series,
    frequency: Frequency,
) -> pd.Series:
    """
    Compute the hit rate on aggregated periods.

    The function aggregates returns at the specified frequency and
    computes the hit rate for each aggregated period. A period is
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
        Time series of hit rate computed on aggregated periods.
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
    - NaN values are ignored. No finite-sample bias correction is applied.

    Let :math:`\\bar{r}` be the sample mean and :math:`s` the
    sample standard deviation.

    The skewness estimator is:

    .. math::

        \\widehat{\\text{Skew}} =
        \\frac{1}{T}
        \\sum_{t=1}^{T}
        \\left(
            \\frac{r_t - \\bar{r}}{s}
        \\right)^3
    """
    arr = np.asarray(returns, dtype=float)
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
    - A normal distribution has zero excess kurtosis.

    - NaN values are ignored. No finite-sample bias correction is applied.

    The excess kurtosis estimator is:

    .. math::

        \\widehat{\\kappa} =
        \\frac{1}{T}
        \\sum_{t=1}^{T}
        \\left(
            \\frac{r_t - \\bar{r}}{s}
        \\right)^4
        - 3
    """
    arr = np.asarray(returns, dtype=float)
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

    Notes
    -----
    - NaN values are ignored.
    - Tracking error is defined as the sample standard deviation of
    active returns:

    Let :math:`a_t = r_t - b_t` denote the active returns.

    The tracking error estimator is:

    .. math::

        \\widehat{\\text{TE}} =
        \\sqrt{
            \\frac{1}{T - 1}
            \\sum_{t=1}^{T}
            (a_t - \\bar{a})^2
        }
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
    -  If the tracking error is zero or undefined, the Information Ratio
    is undefined.

    The Information Ratio estimator is:

    .. math::

        \\widehat{\\text{IR}} =
        \\frac{
            \\bar{a}
        }{
            \\widehat{\\text{TE}}
        }

    where :math:`\\bar{a}` is the sample mean active return and
    :math:`\\widehat{\\text{TE}}` is the tracking error.
    """
    returns_arr = np.asarray(returns, dtype=float)
    factor_arr = np.asarray(factor_returns, dtype=float)

    mask = ~np.isnan(returns_arr) & ~np.isnan(factor_arr)
    returns_arr = returns_arr[mask]
    factor_arr = factor_arr[mask]

    if returns_arr.size < 2:
        return np.nan

    ar = _active_return(returns_arr, factor_arr)
    te = tracking_error(returns_arr, factor_arr)

    if te == 0.0 or np.isnan(te):
        return np.nan

    return float(np.mean(ar) / te)

from __future__ import annotations

from typing import Iterable, Callable, Any
import pandas as pd


def rolling_metric(
    returns: Iterable[float],
    metric: Callable[..., float],
    *,
    window: int,
    min_periods: int | None = None,
    **kwargs: Any,
) -> pd.Series:
    """
    Compute a rolling metric on a sequence of returns.

    The input is internally converted to a pandas Series. If the input
    does not provide a datetime index, a default integer index is used.

    Parameters
    ----------
    returns
        Sequence of periodic returns. If a pandas Series is provided,
        its index is preserved. Otherwise, a default integer index is
        assigned.
    metric
        Metric function to apply. The function must have the
        signature:

            metric(returns: Iterable[float], **kwargs) -> float
    window
        Size of the rolling window, expressed in number of
        observations.
    min_periods
        Minimum number of observations required to compute the
        metric. If None, defaults to `window`.
    **kwargs
        Additional keyword arguments passed directly to `metric`.

    Returns
    -------
    pandas.Series
        Time series of rolling metric values.

    Notes
    -----
    - The rolling operation is index-based, not time-based.
    - If the input does not carry a datetime index, temporal semantics
      (e.g. resampling, calendar alignment) are not available.
    - NaN handling is delegated to the metric function.
    """
    if window <= 0:
        raise ValueError("`window` must be a positive integer.")

    if min_periods is None:
        min_periods = window

    if isinstance(returns, pd.Series):
        series = returns
    else:
        series = pd.Series(list(returns))

    def _apply(x: pd.Series) -> float:
        return metric(x.values, **kwargs)

    return series.rolling(
        window=window,
        min_periods=min_periods,
    ).apply(_apply, raw=False)

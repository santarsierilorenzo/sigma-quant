from typing import Optional, Dict, Any, List, Iterable
from dataclasses import dataclass, field
from statsmodels.stats import diagnostic
from .custom_typing import ArrayLike
from scipy.stats import norm
import numpy as np


@dataclass(frozen=True)
class AutocorrelationTest:
    """
    Container for autocorrelation diagnostic test results.

    Parameters
    ----------
    test_name : str
        Name of the statistical test.
    statistic : float | List[float] | None
        Value(s) of the test statistic. Some tests return one value per lag.
    p_value : float | List[float] | None
        P-value(s) associated with the test statistic.
    reject : bool
        True if the null hypothesis of no autocorrelation is rejected at the
        chosen significance level.
    info : dict[str, Any]
        Additional diagnostic information (e.g. number of lags used,
        degrees of freedom, sample size).
    """
    test_name: str
    statistic: Optional[float | List[float]]
    p_value: Optional[float | List[float]]
    reject: bool
    info: Dict[str, Any] = field(default_factory=dict)


def acf(
    values: ArrayLike,
    lags: int | None = None
) -> np.ndarray:
    """
    Compute sample autocorrelation function.

    Parameters
    ----------
    values : ArrayLike
        Input time series.
    lags : int | None
        Maximum lag. If None, uses floor(log(n)).

    Returns
    -------
    np.ndarray
        Autocorrelations from lag 0 to lag `lags`.
    """

    obs: np.ndarray = np.asarray(values, dtype=float)
    n: int = len(obs)

    if lags is None:
        lags = int(np.log(n))

    mu: float = float(np.mean(obs))
    denom: float = float(np.sum((obs - mu) ** 2))

    rhos: np.ndarray = np.empty(lags + 1)

    rhos[0] = 1.0

    for lag in range(1, lags + 1):
        x_t = obs[lag:]
        x_lag = obs[:-lag]

        num: float = float(np.sum((x_t - mu) * (x_lag - mu)))
        rhos[lag] = num / denom

    return rhos


def bartlett(
    values: ArrayLike,
    lag: int,
    epsilon: float = 0.05
) -> AutocorrelationTest:
    """
    Bartlett test for autocorrelation at a specific lag.

    The test evaluates the null hypothesis that the autocorrelation at a
    given lag is equal to zero.

        H0: rho_k = 0
        H1: rho_k != 0

    The variance of the sample autocorrelation is estimated using
    Bartlett's formula:

        Var(rho_k) ≈ (1 + 2 * sum_{j=1}^{k-1} rho_j^2) / n

    The resulting Z-statistic is asymptotically standard normal.

    Parameters
    ----------
    values : ArrayLike
        Time series observations.
    lag : int
        Lag at which the autocorrelation is tested.
    epsilon : float, default 0.05
        Significance level used for the rejection decision.

    Returns
    -------
    AutocorrelationTest
        Structured container with the estimated autocorrelation,
        test statistic, p-value, and rejection decision.
    """

    obs: np.ndarray = np.asarray(values, dtype=float)
    n: int = len(obs)

    if lag < 1 or lag >= n:
        raise ValueError("Lag must be between 1 and n - 1.")

    rhos: np.ndarray = acf(obs, lags=lag)
    rho_hat: float = float(rhos[lag])

    if lag == 1:
        var_hat: float = 1.0 / n
    else:
        sum_sq: float = float(np.sum(rhos[1:lag] ** 2))
        var_hat = (1.0 + 2.0 * sum_sq) / n

    z_stat: float = rho_hat / np.sqrt(var_hat)
    p_value: float = 2.0 * (1.0 - norm.cdf(abs(z_stat)))

    return AutocorrelationTest(
        test_name="bartlett",
        statistic=z_stat,
        p_value=p_value,
        reject=bool(p_value <= epsilon),
        info={
            "lag": lag,
            "n_obs": n,
            "rho_hat": rho_hat
        }
    )


def ljung_box(
    values: ArrayLike,
    lags: int | None = None,
    boxpierce: bool = False,
    model_df: int = 0,
    epsilon: float = 0.05
) -> AutocorrelationTest:
    """
    Ljung-Box (or Box-Pierce) test for autocorrelation.

    The test evaluates the joint null hypothesis that autocorrelations up to
    a specified lag are equal to zero.

    H0: rho_1 = rho_2 = ... = rho_k = 0
    H1: at least one rho_i != 0

    Parameters
    ----------
    values : Iterable[float]
        Time series observations.
    lags : int | None, default None
        Number of lags included in the test. If None, a default value
        proportional to log(sample_size) is used.
    boxpierce : bool, default False
        If True, compute the Box-Pierce statistic instead of Ljung-Box.
    model_df : int, default 0
        Number of parameters estimated in the model whose residuals are
        being tested. This adjusts the degrees of freedom of the test.
    epsilon : float, default 0.05
        Significance level used for the rejection decision.

    Returns
    -------
    AutocorrelationTest
        Structured container with statistic values, p-values, and the
        rejection decision.

    Notes
    -----
    The Ljung-Box statistic is

        Q = T (T + 2) * sum_{k=1}^h rho_k^2 / (T - k)

    which asymptotically follows a chi-square distribution with
    (h - model_df) degrees of freedom.
    """

    values = np.asarray(values)
    n = len(values)

    if lags is None:
        lags = int(np.log(n))

    test_name = "box_pierce" if boxpierce else "ljung_box"

    results = diagnostic.acorr_ljungbox(
        values,
        lags=lags,
        boxpierce=boxpierce,
        model_df=model_df
    )

    stat_key = "bp_stat" if boxpierce else "lb_stat"
    pval_key = "bp_pvalue" if boxpierce else "lb_pvalue"

    stat = np.asarray(results[stat_key])
    pval = np.asarray(results[pval_key])

    return AutocorrelationTest(
        test_name=test_name,
        statistic=stat.tolist(),
        p_value=pval.tolist(),
        reject=bool(np.any(pval <= epsilon)),
        info={"lags": lags, "model_df": model_df}
    )

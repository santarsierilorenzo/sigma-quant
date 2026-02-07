from __future__ import annotations

from typing import Literal, Iterable, Union
import pandas as pd
import numpy as np

Frequency = Literal["D", "W", "M", "Y"]

ArrayLike = Union[
    Iterable[float],
    np.ndarray,
    pd.Series,
]

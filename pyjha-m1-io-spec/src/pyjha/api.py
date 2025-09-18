import os
from collections.abc import Iterable
from typing import Any, Protocol

import pandas as pd

from .io import use
from .spec import parse_spec


class _FitOlsSig(Protocol):
    def __call__(
        self,
        y: Any,
        X: Any,
        *,
        add_const: bool = True,
        robust: str | None = None,
        weights: Any = None,
        cluster_groups: Any = None,
        hac_maxlags: int | None = None,
    ) -> Any: ...


# declare the name once for mypy; assign below
fit_ols: _FitOlsSig

try:
    # available when pyjha.models is present
    from .models.ols import fit_ols as _fit_ols_impl

    fit_ols = _fit_ols_impl
except Exception as _exc:  # pragma: no cover
    _ERR = f"pyjha.models.ols not available: {_exc!r}"

    def _fit_ols_fallback(
        y: Any,
        X: Any,
        *,
        add_const: bool = True,
        robust: str | None = None,
        weights: Any = None,
        cluster_groups: Any = None,
        hac_maxlags: int | None = None,
    ) -> Any:
        raise ImportError(_ERR)

    fit_ols = _fit_ols_fallback


def _parse_formula(design: str) -> tuple[str, list[str]]:
    if "~" not in design:
        raise ValueError("design must look like 'y ~ x1 + x2 + ...'")
    lhs, rhs = design.split("~", 1)
    y = lhs.strip()
    xs = [c.strip() for c in rhs.split("+") if c.strip()]
    if not y or not xs:
        raise ValueError("invalid design: ensure both y and at least one x are provided")
    return y, xs


def _ensure_df(data: "pd.DataFrame | str | os.PathLike[str]") -> pd.DataFrame:
    if isinstance(data, pd.DataFrame):
        return data
    return use(str(data))


def run(
    data: "pd.DataFrame | str | os.PathLike[str]",
    design: str | None = None,
    *,
    y: str | None = None,
    X: Iterable[str] | None = None,
    add_const: bool = True,
    robust: str | None = None,
    weights: pd.Series | None = None,
    cluster_groups: pd.Series | None = None,
    hac_maxlags: int | None = None,
):
    """Run a simple OLS pipeline.

    Accepts a DataFrame or a filesystem path to CSV/Excel.

    Examples
    --------
    >>> run(df, "y ~ x1 + x2")
    >>> run(df, y="y", X=["x1", "x2"], robust="HC1")
    """
    df = _ensure_df(data)

    if design:
        y_col, x_cols = _parse_formula(design)
    else:
        if not y or not X:
            raise ValueError("provide either design='y ~ x1 + x2' or both y and X")
        y_col, x_cols = y, list(X)

    yv = df[y_col]
    Xv = df[list(x_cols)]

    return fit_ols(
        yv,
        Xv,
        add_const=add_const,
        robust=robust,
        weights=weights,
        cluster_groups=cluster_groups,
        hac_maxlags=hac_maxlags,
    )


__all__ = ["use", "parse_spec", "run"]

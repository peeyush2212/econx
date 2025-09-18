from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

import pandas as pd
import statsmodels.api as sm


@dataclass
class OLSResult:
    params: pd.Series
    bse: pd.Series
    pvalues: pd.Series
    rsquared: float
    nobs: int
    df_model: float
    df_resid: float
    fvalue: Optional[float]
    aic: Optional[float]
    bic: Optional[float]
    _res: Any

    def conf_int(self, alpha: float = 0.05) -> pd.DataFrame:
        return self._res.conf_int(alpha=alpha)

    def summary(self) -> str:
        return self._res.summary().as_text()


def fit_ols(
    y,
    X,
    *,
    add_const: bool = True,
    robust: Optional[str] = None,
    weights=None,
    cluster_groups=None,
    hac_maxlags: Optional[int] = None,
):
    if add_const and "const" not in X.columns:
        X = X.copy()
        X.insert(0, "const", 1.0)
    if weights is not None:
        model = sm.WLS(y, X, weights=weights, missing="drop")
    else:
        model = sm.OLS(y, X, missing="drop")
    res = model.fit()
    if robust:
        if robust.lower() == "cluster":
            if cluster_groups is None:
                raise ValueError("cluster_groups required for cluster robust")
            res = res.get_robustcov_results(cov_type="cluster", groups=cluster_groups)
        elif robust.lower() == "hac":
            res = res.get_robustcov_results(
                cov_type="HAC", maxlags=(hac_maxlags or 1), use_correction=True
            )
        else:
            res = res.get_robustcov_results(cov_type=robust)
    return OLSResult(
        params=res.params,
        bse=res.bse,
        pvalues=res.pvalues,
        rsquared=float(getattr(res, "rsquared", float("nan"))),
        nobs=int(getattr(res, "nobs", 0)),
        df_model=float(getattr(res, "df_model", float("nan"))),
        df_resid=float(getattr(res, "df_resid", float("nan"))),
        fvalue=(None if res.fvalue is None else float(res.fvalue)),
        aic=(None if res.aic is None else float(res.aic)),
        bic=(None if res.bic is None else float(res.bic)),
        _res=res,
    )

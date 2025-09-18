import numpy as np
import pandas as pd
from pyjha.api import run
from pyjha.model.ols import fit_ols
from pyjha.spec.design import build_matrices


def _toy_df():
    x1 = np.array([0, 1, 2, 3, 4, 5], dtype=float)
    x2 = np.array([1, 0, 2, 1, 2, 3], dtype=float)
    y = 1 + 2 * x1 + 3 * x2
    return pd.DataFrame({"y": y, "x1": x1, "x2": x2})


def test_build_matrices_const():
    df = _toy_df()
    y, X = build_matrices(df, "y ~ x1 + x2", add_const=True)
    assert "const" in X.columns and X.shape[0] == len(df)


def test_fit_ols_exact():
    df = _toy_df()
    y, X = build_matrices(df, "y ~ x1 + x2", add_const=True)
    res = fit_ols(y, X, add_const=False)
    got = res.params.round(6).to_dict()
    assert got == {"const": 1.0, "x1": 2.0, "x2": 3.0}


def test_api_run_e2e(tmp_path):
    df = _toy_df()
    p = tmp_path / "t.csv"
    df.to_csv(p, index=False)
    res = run(p, "y ~ x1 + x2")
    got = {k: float(v) for k, v in res.params.round(6).to_dict().items()}
    assert got["const"] == 1.0 and got["x1"] == 2.0 and got["x2"] == 3.0

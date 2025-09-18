from __future__ import annotations

from typing import Union

import pandas as pd


def build_matrices(
    df: pd.DataFrame, spec: Union[str, tuple[str, list[str]]], *, add_const: bool = True
):
    from .parser import parse_spec

    if isinstance(spec, str):
        y_name, x_names = parse_spec(spec)
    else:
        y_name, x_names = spec
    cols = [y_name] + list(x_names)
    df2 = df.loc[:, cols].dropna(axis=0, how="any").copy()
    y = df2[y_name]
    X = df2.drop(columns=[y_name])
    if add_const and "const" not in X.columns:
        X.insert(0, "const", 1.0)
    return y, X

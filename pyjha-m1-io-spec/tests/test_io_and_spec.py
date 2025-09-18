import pandas as pd
from pyjha.io import use
from pyjha.spec import parse_spec


def test_use_csv(tmp_path):
    df = pd.DataFrame({"y": [1, 2, 3, 4], "x1": [10, 20, 30, 40], "x2": [5, 6, 7, 8]})
    p = tmp_path / "d.csv"
    df.to_csv(p, index=False)
    out = use(p, vars=["y", "x2"], rows="1:3", query="x2 >= 6")
    assert list(out.columns) == ["y", "x2"]
    assert out.shape == (2, 2)


def test_use_excel(tmp_path):
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    p = tmp_path / "d.xlsx"
    df.to_excel(p, index=False)
    out = use(p, vars=["b"], rows=[0, 2])
    assert out.shape == (2, 1)
    assert out["b"].iloc[0] == 4


def test_parse_spec():
    y, xs = parse_spec("y ~ x1 + x2 + 1")
    assert y == "y" and xs == ["x1", "x2"]

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Union

import pandas as pd

RowsLike = Union[slice, Sequence[int], tuple[int, int], tuple[int, int, int], str, None]


def _parse_rows(rows: RowsLike) -> slice | list[int] | None:
    if rows is None:
        return None
    if isinstance(rows, slice):
        return rows
    if isinstance(rows, tuple):
        if len(rows) == 2:
            a, b = rows
            return slice(a, b)
        if len(rows) == 3:
            a, b, c = rows
            return slice(a, b, c)
    if isinstance(rows, str):
        parts = [p.strip() for p in rows.split(":")]
        vals = [int(p) if p else None for p in parts]
        if len(vals) == 2:
            return slice(vals[0], vals[1])
        if len(vals) == 3:
            return slice(vals[0], vals[1], vals[2])
        raise ValueError("rows string looks like 'start:stop[:step]'")
    try:
        return [int(i) for i in rows]  # type: ignore[arg-type]
    except Exception as exc:  # noqa: BLE001
        raise TypeError("rows must be slice, tuple, list[int], or 'a:b[:c]'") from exc


def use(
    path: str | Path,
    *,
    vars: Sequence[str] | None = None,
    rows: RowsLike = None,
    query: str | None = None,
) -> pd.DataFrame:
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext in {".xls", ".xlsx"}:
        df = pd.read_excel(path)
    else:
        raise ValueError("Only .csv, .xls, .xlsx supported")
    if vars is not None:
        missing = [c for c in vars if c not in df.columns]
        if missing:
            raise KeyError(f"Columns not found: {missing}")
        df = df[list(vars)]
    if rows is not None:
        r = _parse_rows(rows)
        df = df.iloc[r] if isinstance(r, slice) else df.iloc[r]
    if query:
        df = df.query(query, engine="python")
    return df.reset_index(drop=True)

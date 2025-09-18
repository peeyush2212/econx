from __future__ import annotations


def parse_spec(spec: str) -> tuple[str, list[str]]:
    s = spec.strip()
    if "~" in s:
        left, right = s.split("~", 1)
        y = left.strip()
        rhs = [p.strip() for p in right.split("+")]
        xs = [c for c in rhs if c and c != "1"]
        if not y or not xs:
            raise ValueError("invalid formula")
        return y, xs
    parts = s.split()
    if len(parts) < 2:
        raise ValueError("need dependent and at least one regressor")
    return parts[0], parts[1:]

"""econx: Stata-like econometrics interface (time series & panel).

This is the M0 bootstrap. Actual econometric functionality will be added in later milestones.
"""

from __future__ import annotations

__all__ = ["__version__", "about"]

__version__ = "0.1.0a0"


def about() -> str:
    """Return a short package description."""
    return (
        "econx 0.1.0a0 — Stata-like econometrics (time series & panel) "
        "wrapping statsmodels/linearmodels. (M0 scaffold)"
    )

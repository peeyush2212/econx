# econx (M0 bootstrap)

A **Stata-like econometrics** package focused on **time series** and **panel data**, built on
top of `statsmodels` and `linearmodels`. This is the **M0 scaffold** (project bootstrap).



## Quick start (local)

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (Powershell):
# .venv\Scripts\Activate.ps1

pip install -U pip
pip install -e ".[dev]"  # install package + dev tools
pre-commit install        # enable git hooks (ruff/black etc.)

pytest     # run tests
ruff check .
black --check .
mypy .
```

## Build & Publish (manual)
```bash
python -m build
twine upload --repository testpypi dist/*
# install from TestPyPI:
pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple econx
```

## License
MIT

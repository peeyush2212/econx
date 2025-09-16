import nox

PYTHONS = ["3.10", "3.11", "3.12"]

@nox.session(python=PYTHONS)
def tests(session):
    session.install("-e", ".[dev]")
    session.run("pytest", "-q")

@nox.session(python=PYTHONS)
def lint(session):
    session.install("-e", ".[dev]")
    session.run("ruff", "check", ".")
    session.run("black", "--check", ".")

@nox.session(python=PYTHONS)
def typecheck(session):
    session.install("-e", ".[dev]")
    session.run("mypy", ".")

@nox.session(python=PYTHONS)
def build(session):
    session.install("build")
    session.run("python", "-m", "build")

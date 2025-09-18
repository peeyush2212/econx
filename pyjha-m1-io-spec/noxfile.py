import nox


@nox.session
def tests(session):
    session.install(".[dev]")
    session.run("pytest", "-q")


@nox.session
def lint(session):
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session
def typecheck(session):
    session.install("mypy")
    session.run("mypy", ".")


@nox.session
def format(session):
    session.install("black")
    session.run("black", "--check", ".")

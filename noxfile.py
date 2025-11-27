# noxfile.py
import nox
from pathlib import Path

# Python versions to test
python_versions = ["3.13"]

# Automatically find all subdirectories containing code
SUBPROJECTS = [str(p) for p in Path(".").iterdir() if p.is_dir()]

@nox.session(python=python_versions)
def lint(session):
    """Run ruff linting across all subprojects."""
    session.run("ruff", *SUBPROJECTS)


@nox.session(python=python_versions)
def format(session):
    """Auto-format code with ruff --fix across all subprojects."""
    session.run("ruff", "--fix", *SUBPROJECTS)


@nox.session(python=python_versions)
def typecheck(session):
    """Run type checking using ruff across all subprojects."""
    session.run("ruff", "--select", "TYP", *SUBPROJECTS)

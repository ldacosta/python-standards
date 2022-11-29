"""Invoke tasks"""
import filecmp
import shutil
import sys
import tempfile

from invoke import task


@task
def lint(context):
    """Lint code."""
    context.run("mypy .", pty=True)
    context.run("flake8 --docstring-convention google")
    context.run("pylint -j 4 platypus-core")


@task
def check_format(context):
    """Checks format of code, doesn't format anything."""
    context.run("black . --check")
    context.run("isort . --check")


@task
def format_code(context):
    """Format code."""
    context.run("black .")
    context.run("isort .")


@task
def test(context):
    """Run all tests while checking for code coverage.

    Pty=True to show colors in terminal.
    Note: tests will fail if test coverage is under 80%
    """
    context.run(
        'pytest --durations=10 --cov=. --cov-fail-under=80 --cov-report xml:coverage.xml --cov-config=.coveragerc -m "not benchmark"',
        pty=True,
    )


@task
def create_new_benchmarks(context):
    """Create new benchmarks"""

    context.run("pytest --benchmark-save=platypus-core")


@task
def benchmark(context):
    """Run all benchmark tests to check for performance regressions.

    Pty=True to show colors in terminal.
    Note: benchmark tests will fail if mean time is 0.01 seconds slower for any test
    """
    context.run(
        "pytest --benchmark-compare --benchmark-warmup --benchmark-compare-fail=mean:0.01 -m benchmark",
        pty=True,
    )


@task
def build_docker_image(context, name):
    """Build docker image"""
    context.run(f"docker build . --tag {name}")


@task
def test_docker_image(context, name):
    """Runs docker image tests"""
    context.run(f"./test_docker.sh {name}")


@task
def lock_dependencies(context, use_mamba=False):
    """Create the conda lock file.
    Note: mamba defaults to false because it is possible that it's not installed on a dev's machine."""
    mamba_arg = "--mamba" if use_mamba else ""
    context.run(
        f"conda-lock --strip-auth {mamba_arg} -f environment.yml -p linux-64 -k explicit"
    )

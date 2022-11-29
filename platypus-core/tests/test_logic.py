"""Tests for the logic module."""
import pytest
from logic import add_constant


def test_add_constant():
    """Test add_constant."""
    assert add_constant(1) == 4


@pytest.mark.benchmark
def test_benchmark_add(benchmark):
    """Benchmark add_constant."""
    benchmark(add_constant, 1)

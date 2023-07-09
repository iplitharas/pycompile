"""
Test cases for the `Benchmark`
"""
import logging
from unittest.mock import ANY, MagicMock, patch

import pytest

from src import CythonWrapper, NuitkaWrapper
from src.benchmark import Benchmark

MODULE = "src.benchmark"


@patch(MODULE + ".run_pytest")
@patch(MODULE + ".decorate_functions")
def test_benchmark_run_cpu_bench(
    mocked_decorate_functions,
    mocked_run_pytest,
    sample_python_file_with_test_fixture,
    caplog,
):
    """
    Given one `.py` file with a  test file within a directory
    When we invoke the `cpu_bench` from `Benchmark`
    Then we expect to see the `cpu_bench` in the logs,
    the `decorate_functions` and the run_pytest to be called once.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    assert len(list(sample_folder.iterdir())) == 2
    # When
    Benchmark.cpu_bench(input_path=sample_folder, engine="python")
    # Then
    assert "CPU benchmark using:`python`" in caplog.text
    mocked_decorate_functions.assert_called_once()
    mocked_run_pytest.assert_called_once()


@patch(MODULE + ".run_pytest")
@patch(MODULE + ".decorate_functions")
def test_benchmark_run_memory_bench(
    mocked_decorate_functions,
    mocked_run_pytest,
    sample_python_file_with_test_fixture,
    caplog,
):
    """
    Given one `.py` file with a  test file within a directory
    When we invoke the `mem_bench` from `Benchmark`
    Then we expect to see the `mem_bench` in the logs,
    the `decore_functions` and the `run_pytest` be called once
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    assert len(list(sample_folder.iterdir())) == 2
    # When
    Benchmark.mem_bench(
        input_path=sample_folder, prof_func_name="test", engine="python"
    )
    # Then
    assert "Memory benchmark using:`python`" in caplog.text
    mocked_decorate_functions.assert_called_once()
    mocked_run_pytest.assert_called_once()


def test_benchmark_start_with_bench_type_both_and_without_compiling(
    sample_python_file_with_test_fixture,
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with an empty compilers list
         and a `bench_type` of `both`
    Then we expect only a mem and cpu benchmark to be executed.
    """
    # Given
    sample_folder = sample_python_file_with_test_fixture
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.mem_bench = MagicMock()
    benchmark.cpu_bench = MagicMock()
    benchmark.start(bench_type="both", compilers=[])
    # Then
    benchmark.mem_bench.assert_called_once()
    benchmark.cpu_bench.assert_called_once()


@pytest.mark.parametrize(
    "compilers, expected_compile_calls, expected_mem_bench_calls, expected_cpu_bench_calls",
    [
        (
            [CythonWrapper(), NuitkaWrapper()],
            (ANY, ANY),
            (ANY, ANY, ANY),
            (ANY, ANY, ANY),
        ),
        ([NuitkaWrapper()], (ANY,), (ANY, ANY), (ANY, ANY)),
        ([CythonWrapper()], (ANY,), (ANY, ANY), (ANY, ANY)),
    ],
)
def test_benchmark_start_with_bench_type_both(
    compilers,
    expected_compile_calls,
    expected_mem_bench_calls,
    expected_cpu_bench_calls,
    sample_python_file_with_test_fixture,
    caplog,
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython and Nuitka
         and a `bench_type` of `both`
    Then we expect the `compile`,  `mem_bench` and the `cpu_bench` to be executed
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    assert len(list(sample_folder.iterdir())) == 2
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.mem_bench = MagicMock()
    benchmark.cpu_bench = MagicMock()
    benchmark._compile = MagicMock()
    benchmark.start(bench_type="both", compilers=compilers)
    # Then
    benchmark._compile.assert_has_calls(expected_compile_calls, any_order=True)
    benchmark.mem_bench.assert_has_calls(
        expected_mem_bench_calls, any_order=True
    )
    benchmark.cpu_bench.assert_has_calls(
        expected_cpu_bench_calls, any_order=True
    )


@pytest.mark.parametrize(
    "compilers, expected_compile_calls, expected_mem_bench_calls",
    [
        ([CythonWrapper(), NuitkaWrapper()], (ANY, ANY), (ANY, ANY, ANY)),
        ([NuitkaWrapper()], (ANY,), (ANY, ANY)),
        ([CythonWrapper()], (ANY,), (ANY, ANY)),
    ],
)
def test_benchmark_start_with_bench_type_mem_only(
    compilers,
    expected_compile_calls,
    expected_mem_bench_calls,
    sample_python_file_with_test_fixture,
    caplog,
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method
        and a `bench_type` of `memory`
    Then we expect the `compile`  and `mem_bench` to be executed
         and the `cpu_bench` to be skipped.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.mem_bench = MagicMock()
    benchmark.cpu_bench = MagicMock()
    benchmark._compile = MagicMock()
    benchmark.start(bench_type="memory", compilers=compilers)
    # Then
    benchmark._compile.assert_has_calls(expected_compile_calls, any_order=True)
    benchmark.mem_bench.assert_has_calls(
        expected_mem_bench_calls, any_order=True
    )
    benchmark.cpu_bench.assert_not_called()


@pytest.mark.parametrize(
    "compilers, expected_compile_calls, expected_cpu_bench_calls",
    [
        ([CythonWrapper(), NuitkaWrapper()], (ANY, ANY), (ANY, ANY, ANY)),
        ([NuitkaWrapper()], (ANY,), (ANY, ANY)),
        ([CythonWrapper()], (ANY,), (ANY, ANY)),
    ],
)
def test_benchmark_start_with_bench_type_cpu_only(
    compilers,
    expected_compile_calls,
    expected_cpu_bench_calls,
    sample_python_file_with_test_fixture,
    caplog,
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method  and a `bench_type` of `cpu`
    Then we expect the `compile` and `cpu_bench` to be executed
         and the `mem_bench` to be skipped.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.mem_bench = MagicMock()
    benchmark.cpu_bench = MagicMock()
    benchmark._compile = MagicMock()
    benchmark.start(bench_type="cpu", compilers=compilers)
    # Then
    benchmark._compile.assert_has_calls(expected_compile_calls, any_order=True)
    benchmark.cpu_bench.assert_has_calls(
        expected_cpu_bench_calls, any_order=True
    )
    benchmark.mem_bench.assert_not_called()

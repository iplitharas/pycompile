"""
Test cases for the `Benchmark`
"""
import logging
from unittest.mock import ANY, MagicMock, call, patch

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
    the `decorate_functions`
    and the run_pytest to be called once.
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
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with an empty compilers list
         and a `bench_type` of `both`
    Then we expect only a mem and cpu benchmark to be executed.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    assert len(list(sample_folder.iterdir())) == 2
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.start(bench_type="both", compilers=[])
    # Then
    assert "Memory benchmark" in caplog.text
    assert "CPU benchmark" in caplog.text


def test_benchmark_start_with_bench_type_both_and_with_cython_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython
         and a `bench_type` of `both`
    Then we expect only a mem and cpu benchmark to be executed twice
        one for python and one for cython.
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
    benchmark.start(bench_type="both", compilers=[CythonWrapper()])
    # Then
    benchmark._compile.assert_called_once()
    benchmark.mem_bench.assert_has_calls((ANY, ANY), any_order=True)
    benchmark.cpu_bench.assert_has_calls((ANY, ANY), any_order=True)


def test_benchmark_start_with_bench_type_both_and_with_cython__and_nuitka_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython and Nuitka
         and a `bench_type` of `both`
    Then we expect only a mem and cpu benchmark to be executed three times
        one for python, one for cython and one for nuitka.
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
    benchmark.start(
        bench_type="both", compilers=[CythonWrapper(), NuitkaWrapper()]
    )
    # Then
    benchmark._compile.assert_has_calls((ANY, ANY), any_order=True)
    benchmark.mem_bench.assert_has_calls((ANY, ANY, ANY), any_order=True)
    benchmark.cpu_bench.assert_has_calls((ANY, ANY, ANY), any_order=True)


def test_benchmark_start_with_bench_type_memory_and_without_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with an empty compilers list
        and a `bench_type` of `memory`
    Then we expect only a mem benchmark to be executed.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.start(bench_type="memory", compilers=[])
    # Then
    assert "Memory benchmark" in caplog.text
    assert "CPU benchmark" not in caplog.text


def test_benchmark_start_with_bench_type_memory_and_with_cython__and_nuitka_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython
        and a `bench_type` of `memory`
    Then we expect only a mem benchmark to be executed the times
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
    benchmark.start(
        bench_type="memory", compilers=[CythonWrapper(), NuitkaWrapper()]
    )
    # Then
    benchmark._compile.assert_has_calls((ANY, ANY), any_order=True)
    benchmark.mem_bench.assert_has_calls((ANY, ANY, ANY), any_order=True)
    benchmark.cpu_bench.assert_not_called()


def test_benchmark_start_with_bench_type_memory_and_with_cython_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython
        and a `bench_type` of `memory`
    Then we expect only a mem benchmark to be executed twice
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
    benchmark.start(bench_type="memory", compilers=[CythonWrapper()])
    # Then
    benchmark._compile.assert_called_once()
    benchmark.mem_bench.assert_has_calls((ANY, ANY), any_order=True)
    benchmark.cpu_bench.assert_not_called()


def test_benchmark_start_with_bench_type_cpu_and_without_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with an empty compilers list
        and a `bench_type` of `cpu`
    Then we expect only a cpu benchmark to be executed.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.INFO)
    sample_folder = sample_python_file_with_test_fixture
    # When
    benchmark = Benchmark(input_path=sample_folder)
    benchmark.start(bench_type="cpu", compilers=[])
    # Then
    assert "Memory benchmark" not in caplog.text
    assert "CPU benchmark" in caplog.text


def test_benchmark_start_with_bench_type_cpu_and_with_cython_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython
        and a `bench_type` of `cpu`
    Then we expect only a cpu benchmark to be executed twice
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
    benchmark.start(bench_type="cpu", compilers=[CythonWrapper()])
    # Then
    benchmark._compile.assert_called_once()
    benchmark.cpu_bench.assert_has_calls((ANY, ANY), any_order=True)
    benchmark.mem_bench.assert_not_called()


def test_benchmark_start_with_bench_type_cpu_and_with_cython_and_nuitka_compiling(
    sample_python_file_with_test_fixture, caplog
):
    """
    Given one `.py` file with a test file within a directory.
    When we invoke the `start` method with compilers Cython and Nuitka
        and a `bench_type` of `cpu`
    Then we expect only a cpu benchmark to be executed three times
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
    benchmark.start(
        bench_type="cpu", compilers=[CythonWrapper(), NuitkaWrapper()]
    )
    # Then
    benchmark._compile.assert_has_calls((ANY, ANY), any_order=True)
    benchmark.cpu_bench.assert_has_calls((ANY, ANY, ANY), any_order=True)
    benchmark.mem_bench.assert_not_called()

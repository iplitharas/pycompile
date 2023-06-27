"""
Benchmark implementation
"""
import logging
import sys
from pathlib import Path
from typing import Sequence

from src import CompilerWrapper
from src.compiler_handler import CompilerHandler
from src.file_handler import FileHandler
from src.helpers import Colors, copy_files, decorate_functions, run_pytest

logger = logging.getLogger(__name__)


class Benchmark:
    """
    Runs a benchmarks (memory, cpu)  with (``python``, ``Cython``, ``Nuitka``)
    on ``input_path``  files using the:

    * ``benchmark`` pytest fixture from ``pytest-benchmark`` framework

    *  ``@profile`` decorator from ``memory-profiler``.

    For ``memory`` benchmark the required directory structure needs to be::

        module
            ├── sample_funcs.py                        # implementation
            ├── main.py                                # entrypoint
            ├── test_sample_funcs.py                   # test cases

    where in ``main.py`` we call any functions from ``sample.funcs.py``.
    This is needed because once we compile the ``sample_funcs.py`` we aren't able to use
    the ``profile`` decorator from ``memory-profiler``
    in that case, ``mem_bench`` function will decorate all the
    functions that they match the ``prof_func_name``
    with ``@profile``
    for example::

        def sum_of_squares_benchmark():
            sum_of_squares()



        @profile
        def sum_of_squares_benchmark():
            sum_of_squares()

    For ``cpu`` benchmark the required directory structure needs to be::

          module
            ├── sample_funcs.py                        # implementation
            ├── test_sample_funcs.py                   # test cases


    **NOTES**

    * this way of **memory profiling** isn't accurate (because we don't profile the
      actual python functions), and neither we can do for compiled code
      with python *profiling tools*, but it could be an indicator.

    * The ``test files`` are needed to be able to execute the functions with the right arguments.
    """

    def __init__(self, input_path: Path):
        self.input_path = input_path

    @staticmethod
    def _compile(
        compiler: CompilerWrapper, temp_dir: Path, prof_func_name: str
    ) -> None:
        additional_exclude_patterns = [f"*{prof_func_name}.py"]
        dir_files = FileHandler(
            input_path=temp_dir,
            additional_exclude_patterns=additional_exclude_patterns,
        ).start()
        compiler_handler = CompilerHandler(
            files=dir_files,
            compiler=compiler,
            clean_source=True,
            keep_builds=False,
        )
        compiler_handler.start()

        exe_files = [file.name for file in temp_dir.glob("*.so")]
        test_files = [file.name for file in temp_dir.glob("*.py")]
        logger.debug(
            "%s Running test cases against:%s `%s`  %s test files: %s `%s",
            Colors.CYAN,
            Colors.RESET,
            exe_files,
            Colors.CYAN,
            Colors.RESET,
            test_files,
        )

    @staticmethod
    def mem_bench(input_path: Path, prof_func_name: str, engine: str) -> None:
        """
        decorate all the function(s) from the ``input_path`` where their name match
        the ``prof_func_name`` pattern,
        with the ``@profile`` decorator from ``memory_profiler``.

        Finally, invoke pytest within.
        """
        logger.info(
            "%s Memory benchmark using:`%s` %s",
            Colors.CYAN,
            engine,
            Colors.RESET,
        )
        with copy_files(from_dir=input_path) as temp_dir:
            file_handler = FileHandler(
                input_path=temp_dir,
            )
            files = file_handler.collect_with_pattern("*.py")
            decorate_functions(
                "from memory_profiler import profile",
                "profile",
                files=files,
                func_name_pattern=prof_func_name,
            )
            run_pytest(directory=temp_dir)

    @staticmethod
    def cpu_bench(input_path: Path, engine: str) -> None:
        """
        decorate all the test functions from the ``input_path``
        with the ``@benchmark_wrapper`` decorator.

        Finally, invoke pytest within.
        """
        logger.info(
            "%s CPU benchmark using:`%s` %s",
            Colors.CYAN,
            engine,
            Colors.RESET,
        )
        with copy_files(from_dir=input_path) as temp_dir:
            decorator_def = """def benchmark_wrapper(fn):
                                        def inner(benchmark):
                                            benchmark(fn)
                                        return inner
                        """

            file_handler = FileHandler(
                input_path=temp_dir,
            )
            test_files = file_handler.collect_with_pattern(pattern="*test*.py")
            decorate_functions(
                decorator_def,
                "benchmark_wrapper",
                files=test_files,
                func_name_pattern="test",
            )
            run_pytest(directory=temp_dir)

    def start(
        self,
        bench_type: str,
        compilers: Sequence[CompilerWrapper],
        prof_func_name: str = "benchmark",
    ) -> None:
        """
        Start the benchmark.
        """
        match bench_type:
            case "memory":
                self.mem_bench(
                    input_path=self.input_path,
                    prof_func_name=prof_func_name,
                    engine=sys.version,
                )
            case "cpu":
                self.cpu_bench(input_path=self.input_path, engine=sys.version)
            case "both":
                self.mem_bench(
                    input_path=self.input_path,
                    prof_func_name=prof_func_name,
                    engine=sys.version,
                )
                self.cpu_bench(input_path=self.input_path, engine=sys.version)

        for compiler in compilers:
            with copy_files(from_dir=self.input_path) as temp_dir:
                self._compile(
                    compiler=compiler,
                    temp_dir=temp_dir,
                    prof_func_name=prof_func_name,
                )
                match bench_type:
                    case "memory":
                        self.mem_bench(
                            input_path=temp_dir,
                            prof_func_name=prof_func_name,
                            engine=str(compiler),
                        )
                    case "cpu":
                        self.cpu_bench(
                            input_path=temp_dir, engine=str(compiler)
                        )
                    case "both":
                        self.mem_bench(
                            input_path=temp_dir,
                            prof_func_name=prof_func_name,
                            engine=str(compiler),
                        )
                        self.cpu_bench(
                            input_path=temp_dir, engine=str(compiler)
                        )

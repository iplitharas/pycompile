"""
Benchmark command
"""
import logging
import sys
from pathlib import Path
from typing import Sequence

import click

from src import (
    CompilerCommands,
    CompilerWrapper,
    CythonWrapper,
    NuitkaWrapper,
    setup_logging,
)
from src.benchmark import Benchmark
from src.helpers import Colors

logger = logging.getLogger(__name__)


@click.command(name="benchmark")  # type: ignore[arg-type]
@click.option(
    "-i",
    "--input-path",
    required=True,
    type=click.Path(exists=True),
    help="Specify the file/folder input path",
)
@click.option(
    "-e",
    "--engine",
    default="both",
    help="compiler wrapper(s) to be used for the benchmark, defaults to `both`.",
    type=click.Choice(
        ["cython", "nuitka", "both", "none"], case_sensitive=False
    ),
)
@click.option(
    "-t",
    "--type",
    "bench_type",
    default="both",
    help="type of benchmark to execute, defaults to `both`.",
    type=click.Choice(["memory", "cpu", "both"], case_sensitive=False),
)
@click.option(
    "-p",
    "--profile_func_pattern",
    "prof_func_name",
    default="benchmark",
    help="function name pattern for profiling, "
    "defaults to `benchmark`. "
    "All the functions with a name that matches this pattern "
    "will be decorated with `@profile` from: "
    "`memory-profiler`, in addition their module needs to follow  "
    "the pattern (`something_prof_func_name.py` to be excluded from compilation).",
    type=str,
)
@click.option("-v", "--verbose", count=True, help="verbose level")
def benchmark_cmd(
    input_path: Path,
    engine: str,
    bench_type: str,
    prof_func_name: str,
    verbose: int,
) -> None:
    """
    Run a memory and cpu benchmark.
    """
    setup_logging(verbose)
    input_path = Path(input_path)
    if not input_path.is_dir():
        print(
            f"{Colors.FAIL} Benchmark input path: `{input_path}` needs to "
            f"be a directory, exiting...{Colors.RESET}"
        )
        sys.exit(1)
    benc = Benchmark(input_path=input_path)
    compilers: Sequence[CompilerWrapper] = []
    match engine:
        case "cython":
            compilers = [CythonWrapper(cmd=CompilerCommands.cython_bench)]
        case "nuitka":
            compilers = [NuitkaWrapper(cmd=CompilerCommands.nuitka_bench)]
        case "both":
            compilers = [
                CythonWrapper(cmd=CompilerCommands.cython_bench),
                NuitkaWrapper(cmd=CompilerCommands.nuitka_bench),
            ]
    benc.start(
        compilers=compilers,
        bench_type=bench_type,
        prof_func_name=prof_func_name,
    )

"""
Benchmark implementation:
1) Run the sample test cases using `pytest-benchmark`
2) Compile each sample and re-run the test cases
"""

import logging
import shutil
import sys
import tempfile
from pathlib import Path

import pytest

from src.compiler_handler import CompilerHandler
from src.file_handler import FileHandler
from src.helpers import Colors
from src.wrappers import CompilerCommands, CythonWrapper, NuitkaWrapper

logger = logging.getLogger(__name__)


class Benchmark:
    """
    Runs a benchmark with (`python`, `Cython`, `Nuitka`) on examples  files
    using the `pytest-benchmark`.
    """

    def __init__(self):
        self.dir_files = None
        self.examples_path = None
        self.compilers = [
            CythonWrapper(cmd=CompilerCommands.cython_bench),
            NuitkaWrapper(cmd=CompilerCommands.nuitka_bench),
        ]

    def get_examples(self) -> None:
        """
        Parse all python files at `examples` directory
        """
        self.examples_path = Path(__file__).resolve().parent / "examples"
        if not self.examples_path.exists():
            logger.error(
                "%s examples path `%s` is missing, exiting..%s.",
                Colors.CYAN,
                self.examples_path,
                Colors.RESET,
            )
            sys.exit(1)

        file_handler = FileHandler(
            input_path=self.examples_path,
        )
        self.dir_files = file_handler.start()

    def move_examples(self, temp_dir: Path) -> None:
        """
        Copies all python files in the temp directory.
        """
        for file_path in self.examples_path.glob("*.py"):
            dest_path = temp_dir / file_path.name
            shutil.copy2(file_path, dest_path)

    @staticmethod
    def benchmark(directory: Path) -> None:
        """
        Invoke `pytest` at `directory`
        """
        pytest.main(
            [
                "-vv",
                "--capture=sys",
                "--durations=10",
                directory,
            ]
        )

    def start(self) -> None:
        """
        Start the benchmark for the sample files.
        """
        self.get_examples()
        logger.info(
            "%s Benchmarking python`%s` %s",
            Colors.CYAN,
            sys.version,
            Colors.RESET,
        )
        self.benchmark(directory=self.examples_path)
        for compiler in self.compilers:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                self.move_examples(temp_dir=temp_dir)
                dir_files = FileHandler(
                    input_path=temp_dir,
                ).start()
                compiler_handler = CompilerHandler(
                    files=dir_files,
                    compiler=compiler,
                    clean_source=True,
                    keep_builds=False,
                )
                compiler_handler.start()
                logger.info(
                    "%s Start benchmarking: `%s` %s",
                    Colors.CYAN,
                    str(compiler),
                    Colors.RESET,
                )
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
                self.benchmark(directory=temp_dir)

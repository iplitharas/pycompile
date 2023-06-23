"""
CLI entrypoint.
"""
import logging
import sys
from pathlib import Path

import click

from src import (
    CompilerHandler,
    CythonWrapper,
    FileHandler,
    NuitkaWrapper,
    setup_logging,
)
from src.benchmark import Benchmark
from src.helpers import Colors

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "-i",
    "--input-path",
    required=False,
    type=click.Path(exists=True),
    help="Specify the file/folder input path, "
    "by default it will exclude any `test` and `__ini__.py` files",
)
@click.option(
    "-ex",
    "--exclude-glob-paths",
    required=False,
    multiple=True,
    type=str,
    default=FileHandler(".").exclude_patterns,
    help="glob files patterns of the files to be excluded, example: **/ignore_this_module.py",
)
@click.option("-v", "--verbose", count=True, help="verbose level")
@click.option(
    "-e",
    "--engine",
    default="cython",
    help="CompilerWrapper to be used, defaults to: `cython`",
    type=click.Choice(["cython", "nuitka"], case_sensitive=False),
)
@click.option(
    "-cs",
    "--clean-source",
    "clean_source",
    flag_value=True,
    default=False,
    help="Clean source (.py) files",
)
@click.option(
    "-kb",
    "--keep-builds",
    "keep_builds",
    flag_value=True,
    default=False,
    help="Keep temporary build files",
)
@click.option(
    "-ce",
    "--clean-executables",
    "clean_executables",
    flag_value=True,
    default=False,
    help="Clean final executables (.so) files",
)
@click.option(
    "-b",
    "--benchmark",
    required=False,
    flag_value=True,
    default=False,
    help="Benchmark the examples.",
)
def main(  # pylint: disable=too-many-arguments
    input_path,
    exclude_glob_paths,
    verbose,
    engine,
    clean_source,
    keep_builds,
    clean_executables,
    benchmark,
):
    r"""
                                          _ _
    _ __  _   _  ___ ___  _ __ ___  _ __ (_) | ___
   | '_ \| | | |/ __/ _ \| '_ ` _ \| '_ \| | |/ _ \
   | |_) | |_| | (_| (_) | | | | | | |_) | | |  __/
   | .__/ \__, |\___\___/|_| |_| |_| .__/|_|_|\___|
   |_|    |___/                    |_|
   """
    handle_user_input(
        input_path,
        exclude_glob_paths,
        verbose,
        engine,
        clean_source,
        keep_builds,
        clean_executables,
        benchmark,
    )


def handle_user_input(  # pylint: disable=too-many-arguments
    input_path: Path,
    exclude_glob_paths: list[str],
    verbose: int,
    engine: str,
    clean_source: bool,
    keep_builds: bool,
    clean_executables: bool,
    benchmark: bool,
) -> None:
    """
    Helper function for handling the user input.
    """
    setup_logging(verbose)
    if benchmark:
        bench = Benchmark()
        bench.start()
        sys.exit(0)

    if not input_path:
        logger.error(
            "%s Input path is missing, exiting...%s", Colors.FAIL, Colors.RESET
        )
        sys.exit(1)

    dir_files = FileHandler(
        input_path=input_path,
        additional_exclude_patterns=exclude_glob_paths,
    ).parse_files()

    if dir_files:
        compiler = (
            CythonWrapper() if engine.lower() == "cython" else NuitkaWrapper()
        )
        compiler_handler = CompilerHandler(
            files=dir_files,
            compiler=compiler,
            clean_source=clean_source,
            keep_builds=keep_builds,
        )
        compiler_handler.start()
        if clean_executables:
            compiler_handler.clean_executables()

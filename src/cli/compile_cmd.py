"""
Compile command
"""
import logging
from pathlib import Path

import click

from src import (
    CompilerHandler,
    CythonWrapper,
    FileHandler,
    NuitkaWrapper,
    setup_logging,
)

logger = logging.getLogger(__name__)


@click.command(name="compile")  # type: ignore[arg-type]
@click.option(
    "-i",
    "--input-path",
    required=True,
    type=click.Path(exists=True),
    help="Specify the file/folder input path, "
    "by default it will exclude any `test` and `__init__.py` files",
)
@click.option(
    "-ex",
    "--exclude-glob-paths",
    required=False,
    multiple=True,
    type=str,
    default=FileHandler("..").exclude_patterns,  # type: ignore[arg-type]
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
def compile_cmd(  # pylint: disable=R0913
    input_path: Path,
    exclude_glob_paths: list[str],
    verbose: int,
    engine: str,
    clean_source: bool,
    keep_builds: bool,
    clean_executables: bool,
) -> None:
    """
    Compile the python files using `cython` or `nuitka`.
    """
    setup_logging(verbose)

    dir_files = FileHandler(
        input_path=input_path,
        additional_exclude_patterns=exclude_glob_paths,
    ).start()
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

"""
dry run command
"""
import logging
from pathlib import Path

import click

from src import FileHandler, setup_logging
from src.helpers import Colors

logger = logging.getLogger(__name__)


@click.command(name="dry_run")  # type: ignore[arg-type]
@click.option(
    "-i",
    "--input-path",
    required=True,
    type=click.Path(exists=True),
    help="Specify the file/folder input path",
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
def dry_run_cmd(
    input_path: Path, exclude_glob_paths: list[str], verbose: int
) -> None:
    """
    Perform a dry run.
    """
    setup_logging(verbose)
    file_handler = FileHandler(
        input_path=input_path, additional_exclude_patterns=exclude_glob_paths
    )
    dir_files = file_handler.start()
    if not dir_files:
        print(
            f"{Colors.CYAN} Nothing found at: `{input_path}` path"
            f" using: {file_handler.exclude_patterns}  as glob patterns.."
            f" {Colors.RESET}"
        )
        return

    for dir_name, files in dir_files.items():
        print(f"{Colors.CYAN} {dir_name} {Colors.RESET}")
        render_files(files, is_last=False)


def render_files(
    files: list[Path], indent: str = "", is_last: bool = True
) -> None:
    """
    Render the output in a human-readable format.
    """
    branch = "└── " if is_last else "├── "
    indent += "    "
    for file in files:
        print(f"{indent[:-1]}{branch}{file.name}")

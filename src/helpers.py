"""
implementations for
`change_dir` context manager
and `run_sub_process` helper function.
"""
import os
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Colors:  # pylint: disable=missing-class-docstring
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


@contextmanager
def change_dir(file_path: Path):
    """
    Context manager to change the current active directory at the `file path` parents.
    This is needed to be able to include the compiled files in the
    same directory as the source files.
    """
    current_path = Path().absolute()
    try:
        yield os.chdir(file_path)
    finally:
        os.chdir(current_path)


def run_sub_process(files: list[Path], compile_cmd: str) -> None:
    """
    For each file path runs in a subprocess the corresponding compiler command.
    """
    for file in files:
        cmd_str = compile_cmd.format(file.absolute())
        subprocess.run(cmd_str, shell=True, check=False)

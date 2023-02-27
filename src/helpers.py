"""
implementations for
`change_dir` context manager
and `run_sub_process` helper function.
"""
import os
import subprocess
from contextlib import contextmanager
from pathlib import Path


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
        with change_dir(file_path=file.parent):
            cmd_str = compile_cmd.format(file.absolute())
            subprocess.run(cmd_str, shell=True)

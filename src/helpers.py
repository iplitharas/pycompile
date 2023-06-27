"""
pycompile helper functions.
"""
import ast
import os
import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable

import pytest


@dataclass(frozen=True)
class Colors:
    """
    pycompile colors
    """

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
def change_dir(file_path: Path) -> Generator[None, None, None]:
    """
    Context manager to change the current active directory at the `file path` parents.
    This is needed to be able to include the compiled files in the
    same directory as the source files.
    """
    current_path = Path().absolute()
    try:
        os.chdir(file_path)
        yield
    finally:
        os.chdir(current_path)


@contextmanager
def copy_files(from_dir: Path) -> Generator[Path, None, None]:
    """
    Copies all files at a temp directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree(from_dir, temp_dir, dirs_exist_ok=True)
        yield Path(temp_dir)


def decorate_functions(
    dec_import: str,
    dec_name: str,
    files: Iterable[Path],
    func_name_pattern: str,
) -> None:
    """
    For each file:
    add the `decorator import` at the top level of the file and
    decorate all the functions with the `decorate name`
    """
    for file in files:
        with open(
            file, "r", encoding="utf-8"
        ) as f:  # pylint: disable=invalid-name
            tree = ast.parse(f.read())

        modified_tree = ast.parse("")
        modified_tree.body.extend([ast.parse(dec_import).body[0]])
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if re.search(func_name_pattern, node.name):
                    node.decorator_list.insert(
                        0, ast.Name(id=dec_name, ctx=ast.Load())
                    )

        with open(
            file, "w", encoding="utf-8"
        ) as f:  # pylint: disable=invalid-name
            f.write(ast.unparse(modified_tree))
            f.write("\n\n")
            f.write(ast.unparse(tree))


def run_pytest(directory: Path) -> None:
    """
    Invoke `pytest` at the `directory`.
    """
    pytest.main(
        [
            "-vv",
            "--capture=sys",
            "--durations=10",
            "-s",
            str(directory),
        ]
    )


def run_sub_process(files: list[Path], compile_cmd: str) -> None:
    """
    For each file path run in a subprocess the corresponding compiler command.
    """
    for file in files:
        cmd_str = compile_cmd.format(file.absolute())
        subprocess.run(cmd_str, shell=True, check=False)

"""
Compilers (`Cython` and `Nuitka`) wrapper implementations.
"""
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CompilerCommands:  # pylint: disable=missing-class-docstring
    cython = "cythonize {} -3 --inplace"
    cython_bench = "cythonize {} -3 --inplace --quiet 2>/dev/null"
    nuitka = "python -m nuitka --module {}"
    nuitka_bench = "python -m nuitka --quiet --module {} 2>/dev/null"


class Compiler(ABC):  # pylint: disable=missing-class-docstring
    @property
    @abstractmethod
    def cmd(self):  # pylint: disable=missing-function-docstring
        raise NotImplementedError("Each compiler should have a command!")

    @cmd.setter
    def cmd(self, new_cmd: str):  # pylint: disable=missing-function-docstring
        raise NotImplementedError(
            "Each compiler should be able to set the command!"
        )

    @abstractmethod
    def cleanup(
        self, file_path: Path
    ):  # pylint: disable=missing-function-docstring
        raise NotImplementedError("Each compiler should clean it's mess!")


class CythonCompiler(Compiler):
    """
    Cython is a programming language, a superset of the Python programming language,
    designed to give C-like performance with code that is written mostly in Python with optional
    additional C-inspired syntax.
    Cython is a compiled language that is typically used to generate CPython extension modules
    https://cython.org/
    """

    def __init__(self, cmd: str = CompilerCommands.cython):
        self.cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, new_cmd: str):
        self._cmd = new_cmd

    def cleanup(self, file_path: Path) -> None:
        """
        Deletes the `build`directory.
        """
        build_path = file_path.parent / "build"
        if not build_path.exists():
            build_path = file_path.parent.parent / "build"
        if build_path.exists():
            shutil.rmtree(build_path)

        c_extension = file_path.with_suffix(".c")
        c_extension.unlink(missing_ok=True)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class NuitkaCompiler(Compiler):
    """
    Nuitka is a source-to-source compiler which compiles Python code to C source code,
    applying some compile-time optimizations in the process such as constant
    folding and propagation,
    built-in call prediction, type inference, and conditional statement execution.
    https://nuitka.net/
    """

    def __init__(self, cmd: str = CompilerCommands.nuitka):
        self.cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, new_cmd: str):
        self._cmd = new_cmd

    def cleanup(self, file_path: Path):
        """
        Deletes the `build`directory alongside with the `file.pyi` temp file.
        """
        build_path = file_path.with_suffix(".build")
        if build_path.exists():
            shutil.rmtree(build_path)
        pyi_extension = file_path.with_suffix(".pyi")
        pyi_extension.unlink(missing_ok=True)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

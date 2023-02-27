"""
Compilers (`Cython` and `Nuitka`) wrapper implementations.
"""
import shutil
from abc import ABC, abstractmethod
from pathlib import Path


class Compiler(ABC):
    @property
    @abstractmethod
    def cmd(self):
        raise NotImplementedError("Each compiler should have a command!")

    @cmd.setter
    def cmd(self, new_cmd: str):
        raise NotImplementedError("Each compiler should be able to set the command!")

    @abstractmethod
    def cleanup(self, file_path: Path):
        raise NotImplementedError("Each compiler should clean it's mess!")


class CythonCompiler(Compiler):
    """
    Cython is a programming language, a superset of the Python programming language,
    designed to give C-like performance with code that is written mostly in Python with optional
    additional C-inspired syntax.
    Cython is a compiled language that is typically used to generate CPython extension modules
    https://cython.org/
    """

    def __init__(self, cmd: str = "cythonize {} -3 --inplace"):
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


class NuitkaCompiler(Compiler):
    """
    Nuitka is a source-to-source compiler which compiles Python code to C source code,
    applying some compile-time optimizations in the process such as constant folding and propagation,
    built-in call prediction, type inference, and conditional statement execution.
    https://nuitka.net/
    """

    def __init__(self, cmd: str = "python -m nuitka --module {}"):
        self.cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, new_cmd: str):
        self._cmd = new_cmd

    def cleanup(self, file_path: Path):
        """
        Deletes the `build`directory alongside with the `file.pyi` temp
        file.
        """
        build_path = file_path.with_suffix(".build")
        if build_path.exists():
            shutil.rmtree(build_path)
        pyi_extension = file_path.with_suffix(".pyi")
        pyi_extension.unlink(missing_ok=True)

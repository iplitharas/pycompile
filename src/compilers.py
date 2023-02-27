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
    def __init__(self, cmd: str = "cythonize {} -3 --inplace"):
        self.cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, new_cmd: str):
        self._cmd = new_cmd

    def cleanup(self, file_path: Path):
        build_path = file_path.parent / "build"
        if not build_path.exists():
            build_path = file_path.parent.parent / "build"
        if build_path.exists():
            shutil.rmtree(build_path)

        c_extension = file_path.with_suffix(".c")
        c_extension.unlink(missing_ok=True)


class NuitkaCompiler(Compiler):
    def __init__(self, cmd: str = "python -m nuitka --module {}"):
        self.cmd = cmd

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, new_cmd: str):
        self._cmd = new_cmd

    def cleanup(self, file_path: Path):
        build_path = file_path.with_suffix(".build")
        if build_path.exists():
            shutil.rmtree(build_path)
        pyi_extension = file_path.with_suffix(".pyi")
        pyi_extension.unlink(missing_ok=True)

"""
Fake CompilerWrapper implementation.
"""
from pathlib import Path

from src import CompilerWrapper


class FakeCompilerWrapper(CompilerWrapper):
    def __init__(self):
        self.cmd = "stat {}"

    def cleanup(self, file_path: Path):
        pass

    @property
    def cmd(self):
        return self._cmd

    @cmd.setter
    def cmd(self, new_cmd: str):
        self._cmd = new_cmd

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.cmd})"

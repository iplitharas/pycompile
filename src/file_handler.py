"""
FileHandler implementation
Note:
`glob patterns`: `**`:   Recursively matches zero or more directories
                         that fall under the current directory.
                 `*` :   On Unix, will match everything except slashes.
                         On Windows, it will avoid matching backslashes as well as slashes.
"""
import logging
from collections import defaultdict
from pathlib import Path
from typing import Generator

from src.helpers import Colors

logger = logging.getLogger(__name__)


class FileHandler:
    """
    FileHandler is responsible for finding all the `.py` files  given
    any `input_path`.
    example usage: FileHandler("./my_module).start()
    """

    def __init__(
        self,
        input_path: Path | str,
        additional_exclude_patterns: list[str] = None,
    ):
        """
        By default, all the `test` files and any `__init__` files are excluded
        :param `input_path`: Should be a valid file/directory path.
        :param `additional_exclude_patterns`: Any optional additional glob patterns.
        """
        self.input_path = input_path
        self.exclude_patterns = additional_exclude_patterns

    @property
    def input_path(self) -> Path:
        """
        Current `input path`
        """
        return self._input_path

    @input_path.setter
    def input_path(self, path: Path | str) -> None:
        if Path(path).exists():
            self._input_path = Path(path)
        else:
            raise ValueError(f"Path: {Path(path)} doesn't exist...")

    @property
    def exclude_patterns(self):
        """
        Current glob exclude patterns
        """
        return self._exclude_patterns

    @exclude_patterns.setter
    def exclude_patterns(self, additional_exclude_patterns: list[str] | None):
        self._exclude_patterns = [
            "**/test**",
            "**/__init__.py",
        ]

        if additional_exclude_patterns:
            self._exclude_patterns.extend(additional_exclude_patterns)

    def start(self) -> dict[str : list[Path]]:
        """
        For the given `input path` collect all valid `.py` files.
        :return: a dictionary for valid files within each directory.
        """

        files = defaultdict(list[Path])
        excluded_files = list(self._filter_files())
        logger.debug(
            "%sExcluded files: %s%s",
            Colors.CYAN,
            Colors.RESET,
            [
                excluded_file.name
                for excluded_file in excluded_files
                if excluded_file
            ],
        )

        for file in self._collect_files():
            if file not in excluded_files:
                files[str(file.resolve().parent)].append(file.resolve())

        return files

    def _filter_files(self) -> Generator[Path, None, None]:
        """
        Collects all files to be excluded for the given `input path`
        using the `exclude_patterns` glob patterns.
        """
        if not self.input_path.is_dir():
            yield None
        yield from (
            file
            for file in self._collect_files()
            for exclude_pattern in self.exclude_patterns
            if file.match(exclude_pattern)
        )

    def _collect_files(self) -> Generator[Path, None, None]:
        """
        Collects all python files for the given `input path`.
        """
        if not self.input_path.is_dir():
            yield self.input_path

        else:
            for sub_dir in self.input_path.iterdir():
                if sub_dir.is_dir():
                    yield from sub_dir.rglob(pattern="**/*.py")

            yield from self.input_path.glob(pattern="*.py")

    def __str__(self) -> str:
        return (
            f"FileHandler\n"
            f"Input path: {self.input_path}\n"
            f"Exclude glob patters: {self.exclude_patterns}\n"
        )

    def __repr__(self) -> str:
        return (
            f"FileHandler(input_path={self.input_path},"
            f"additional_exclude_patterns={self.exclude_patterns},"
        )

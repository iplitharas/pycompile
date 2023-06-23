"""
`CompilerHandler` implementation
"""
import logging
from pathlib import Path

from tqdm import tqdm

from src.compilers import Compiler
from src.helpers import Colors, change_dir, run_sub_process

logger = logging.getLogger(__name__)


class CompilerHandler:
    """
     CompilerHandler is responsible for compiling all the `.py` files using
    `Cython` or `Nuitka`
    """

    def __init__(
        self,
        files: dict[str : list[Path]],
        compiler: Compiler,
        clean_source: bool = False,
        keep_builds: bool = True,
    ):
        self.files = files
        self.compiler = compiler
        self.clean_source = clean_source
        self.keep_builds = keep_builds

    def clean_executables(self) -> None:
        """
        Cleans all the `.so` files.
        """
        for directory, _ in self.files.items():
            for executable in Path(directory).glob(pattern="*.so"):
                executable.unlink(missing_ok=True)

    def start_compiling(self) -> None:
        """
        For each `.py` file runs the compiler command
        to build the final executable `.so`
        """
        total_iterations = sum(len(files) for files in self.files.values())
        for directory, dir_files in tqdm(
            self.files.items(),
            total=total_iterations,
            ascii=True,
            desc=f"{Colors.CYAN}Compiling using: `{self.compiler}`{Colors.RESET}",
            dynamic_ncols=True,
        ):
            with change_dir(directory):
                try:
                    run_sub_process(
                        files=dir_files, compile_cmd=self.compiler.cmd
                    )
                finally:
                    if not self.keep_builds:
                        self._clean_build_files(files=dir_files)
                    if self.clean_source:
                        self._clean_source_files(files=dir_files)

    @staticmethod
    def _clean_source_files(files: list[Path]) -> None:
        """
        Cleans the `source` files.
        """
        deleted = [file.unlink() for file in files]
        logger.warning(
            "%sFlag `--clean-source` is on, deleted " f"#{len(deleted)}" "%s",
            Colors.CYAN,
            Colors.RESET,
        )

    def _clean_build_files(self, files: list[Path]) -> None:
        """
        Cleans the temporary `build` files.
        """
        for file in files:
            self.compiler.cleanup(file_path=file)
        logger.warning(
            "%s Flag `-keep-builds` is off, all temp build files are deleted.."
            "%s",
            Colors.CYAN,
            Colors.RESET,
        )

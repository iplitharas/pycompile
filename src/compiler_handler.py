"""
CompilerHandler implementation
"""
from pathlib import Path

from tqdm import tqdm

from src import (
    Compiler,
    CythonCompiler,
    NuitkaCompiler,
    FileHandler,
    change_dir,
    run_sub_process,
)


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
        clean_builds: bool = True,
    ):
        self.files = files
        self.compiler = compiler
        self.clean_source = clean_source
        self.clean_builds = clean_builds

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
        for directory, dir_files in tqdm(
            self.files.items(),
            ascii=True,
            desc="Compiling",
            dynamic_ncols=True,
        ):
            try:
                run_sub_process(files=dir_files, compile_cmd=self.compiler.cmd)
            finally:
                self._clean_build_files(files=dir_files)
                self._clean_source_files(files=dir_files)

    def _clean_source_files(self, files: list[Path]) -> None:
        """
        Cleans the `source` files.
        """
        if self.clean_source:
            for file in files:
                with change_dir(file.parent):
                    file.unlink()

    def _clean_build_files(self, files: list[Path]) -> None:
        """
        Cleans the temporary `build` files.
        """
        if self.clean_builds:
            for file in files:
                with change_dir(file.parent):
                    self.compiler.cleanup(file_path=file)


if __name__ == "__main__":
    file_handler = FileHandler(
        Path(
            "../demo/",
        )
        # additional_exclude_patterns=["**/something_else/*.py", "**/yolo2/*.py"],
    )
    input_files = file_handler.parse_files()
    compiler_handler = CompilerHandler(files=input_files, compiler=NuitkaCompiler())
    compiler_handler.start_compiling()
    compiler_handler.clean_executables()

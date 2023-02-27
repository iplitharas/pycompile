from pathlib import Path

import click

from src import CompilerHandler, CythonCompiler, FileHandler, NuitkaCompiler


@click.command()
@click.option(
    "-i",
    "--input-path",
    required=True,
    type=click.Path(exists=True),
    help="Specify the file/folder input path, "
    "by default it will exclude any `test` and `__ini__.py` files",
)
@click.option(
    "-ex",
    "--exclude-glob-paths",
    required=False,
    multiple=True,
    type=str,
    default=FileHandler(".").exclude_patterns,
    help="glob files patterns of the files to be excluded, example: **/ignore_this_module.py",
)
@click.option("-v", "--verbose", count=True, help="verbose level")
@click.option(
    "-e",
    "--engine",
    default="cython",
    help="Compiler to be used, defaults to: `cython`",
    type=click.Choice(["cython", "nuitka"], case_sensitive=False),
)
@click.option(
    "-cs",
    "--clean-source",
    "clean_source",
    flag_value=True,
    default=False,
    help="Clean source (.py) files",
)
@click.option(
    "-kb",
    "--keep-builds",
    "keep_builds",
    flag_value=True,
    default=False,
    help="Keep temporary build files",
)
@click.option(
    "-ce",
    "--clean-executables",
    "clean_executables",
    flag_value=True,
    default=False,
    help="Clean final executables (.so) files",
)
def main(
    input_path,
    exclude_glob_paths,
    verbose,
    engine,
    clean_source,
    keep_builds,
    clean_executables,
):
    """Start compilation of the files"""

    file_handler = FileHandler(
        input_path=input_path,
        additional_exclude_patterns=exclude_glob_paths,
        verbose=True if verbose > 0 else False,
    )
    dir_files = file_handler.parse_files()

    for directory, files in dir_files.items():
        directory_str = (
            str(Path(directory).parent) + "/" + str(Path(directory).name)
        )
        click.echo(
            "🗂️  "
            + click.style(
                text=directory_str + f" with #{len(files)} files", fg="cyan"
            ),
        )
    if dir_files:
        compiler = (
            CythonCompiler() if engine.lower() == "cython" else NuitkaCompiler()
        )
        compiler_handler = CompilerHandler(
            files=dir_files,
            compiler=compiler,
            clean_source=clean_source,
            keep_builds=keep_builds,
        )
        compiler_handler.start_compiling()
        if clean_executables:
            compiler_handler.clean_executables()


# if __name__ == "__main__":
#     main()

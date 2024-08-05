"""
Integration test cases for `CompilerHandler`
using `Cython` and `Nuitka`.
"""

import logging

from src import CompilerHandler, CythonWrapper, NuitkaWrapper


def test_compiler_handler_compiles_using_cython_without_clean_source_and_keep_builds(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `Cython` as a compiler
         and clean_source  and keep_builds are off
    Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)

    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=CythonWrapper(),
        clean_source=False,
        keep_builds=False,
    )
    compiler_handler.start()
    # Then
    assert " Flag `-keep-builds` is off" in caplog.text
    assert len(list(sample_folder.iterdir())) == 2
    source_file = sample_folder / "hello.py"
    assert source_file.is_file()
    build_folder = sample_folder / "build"
    assert not build_folder.is_dir()
    c_file = sample_folder / "hello.c"
    assert not c_file.is_file()


def test_compiler_handler_compiles_using_cython_with_keep_builds_and_without_clean_source(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling` from `CompilerHandler`
         using `Cython` as a compiler
         and clean_source=False and `keep_builds=True`
    Then we expect the right number of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)
    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=CythonWrapper(),
        clean_source=False,
        keep_builds=True,
    )
    compiler_handler.start()
    # Then
    assert len(list(sample_folder.iterdir())) == 3
    assert " Flag `--clean-source` is on" not in caplog.text
    source_file = sample_folder / "hello.py"
    assert source_file.is_file()

    c_file = sample_folder / "hello.c"
    assert c_file.is_file()


def test_compiler_handler_compiles_using_cython_with_clean_source_and_without_keep_build(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `Cython` as a compiler
         and clean_source=True  and keep_builds=False
     Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)

    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=CythonWrapper(),
        clean_source=True,
        keep_builds=False,
    )
    compiler_handler.start()
    # Then
    assert " Flag `-keep-builds` is off" in caplog.text
    assert len(list(sample_folder.iterdir())) == 1
    source_file = sample_folder / "hello.py"
    assert not source_file.is_file()
    build_folder = sample_folder / "build"
    assert not build_folder.is_dir()
    c_file = sample_folder / "hello.c"
    assert not c_file.is_file()


def test_compiler_handler_compiles_using_cython_with_keep_builds_and_clean_source(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `Cython` as a compiler
         and clean_source=True  and keep_builds=True
    Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)

    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=CythonWrapper(),
        clean_source=True,
        keep_builds=True,
    )
    compiler_handler.start()
    # Then
    assert len(list(sample_folder.iterdir())) == 2
    assert " Flag `--clean-source` is on" in caplog.text
    source_file = sample_folder / "hello.py"
    assert not source_file.is_file()
    c_file = sample_folder / "hello.c"
    assert c_file.is_file()


def test_compiler_handler_compiles_using_nuitka_with_clean_source_and_without_keep_build(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `nuitka` as a compiler
         and clean_source=True  and keep_builds=False
     Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)

    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=NuitkaWrapper(),
        clean_source=True,
        keep_builds=False,
    )
    compiler_handler.start()
    # Then
    assert " Flag `-keep-builds` is off" in caplog.text
    assert len(list(sample_folder.iterdir())) == 1
    source_file = sample_folder / "hello.py"
    assert not source_file.is_file()
    temp_build_file = sample_folder / "hello.build"
    assert not temp_build_file.is_file()
    temp_build_file = sample_folder / "hello.pyi"
    assert not temp_build_file.is_file()


def test_compiler_handler_compiles_using_nuitka_with_keep_builds_and_clean_source(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `nuitka` as a compiler
         and clean_source=True  and keep_builds=True
    Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)

    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=NuitkaWrapper(),
        clean_source=True,
        keep_builds=True,
    )
    compiler_handler.start()
    # Then
    assert len(list(sample_folder.iterdir())) == 3
    assert " Flag `--clean-source` is on" in caplog.text
    source_file = sample_folder / "hello.py"
    assert not source_file.is_file()
    temp_build_dir = sample_folder / "hello.build"
    assert temp_build_dir.is_dir()
    temp_build_file = sample_folder / "hello.pyi"
    assert temp_build_file.is_file()


def test_compiler_handler_compiles_using_nuitka_without_clean_source_and_keep_builds(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `nuitka` as a compiler
         and clean_source  and keep_builds are off
    Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)

    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=NuitkaWrapper(),
        clean_source=False,
        keep_builds=False,
    )
    compiler_handler.start()
    # Then
    assert " Flag `-keep-builds` is off" in caplog.text
    assert len(list(sample_folder.iterdir())) == 2
    source_file = sample_folder / "hello.py"
    assert source_file.is_file()
    temp_build_file = sample_folder / ".build"
    assert not temp_build_file.is_file()
    temp_build_file = sample_folder / "hello.pyi"
    assert not temp_build_file.is_file()


def test_compiler_handler_compiles_using_nuitka_with_keep_builds_and_without_clean_source(
    sample_python_file_fixture, caplog
):
    """
    Given some `.py` files within a directory
    When we invoke the `start_compiling`  from `CompilerHandler`
         using `nuitka` as a compiler
         and clean_source=False  and keep_builds=True
    Then we expect the right amount of files.
    """
    # Given
    caplog.clear()
    caplog.set_level(logging.WARNING)
    sample_folder = sample_python_file_fixture
    assert len(list(sample_folder.iterdir())) == 1
    # When
    compiler_handler = CompilerHandler(
        files={str(sample_folder): list(sample_folder.iterdir())},
        compiler=NuitkaWrapper(),
        clean_source=False,
        keep_builds=True,
    )
    compiler_handler.start()
    # Then
    assert len(list(sample_folder.iterdir())) == 4
    assert " Flag `--clean-source` is on" not in caplog.text
    source_file = sample_folder / "hello.py"
    assert source_file.is_file()
    build_folder = sample_folder / "hello.build"
    assert build_folder.is_dir()
    temp_build_file = sample_folder / "hello.pyi"
    assert temp_build_file.is_file()

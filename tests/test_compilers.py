"""
Test cases for `CythonCompiler` and `NuitkaCompiler`.
"""
import pytest

from src import Compiler, CompilerCommands, CythonCompiler, NuitkaCompiler


def test_cython_compiler_cleanup(sample_cython_build_fixture):
    """
    Given a successful cython compile where we have the following structure
    temp-dir
        ├── build         # Cython build temp files
        ├── hello.py      # Python sample test file
        ├── hello.c
        ├── hello.so
    When we call the `cleanup` from the `compiler` with the
          path of original `.py`
    Then we expect the following file structure.
    temp-dir
        ├── hello.py      # Python sample test file
        ├── hello.so
    """
    # Given
    sample_files_path = sample_cython_build_fixture
    assert len(list(sample_files_path.iterdir())) == 4
    # When
    cython_compiler = CythonCompiler()
    cython_compiler.cleanup(file_path=sample_files_path / "hello.py")
    # Then
    assert len(list(sample_files_path.iterdir())) == 2


def test_nuitka_compiler_cleanup(sample_nuitka_build_fixture):
    """
    Given a successful `nuitka` compile where we have the following structure
    temp-dir
        ├── hello.build/         # Nuitka build temp files
        ├── hello.py        # Python sample test file
        ├── hello.pyi       # Nuitka intermediate build file
        ├── hello.so
    When we call the `cleanup` from the `compiler` with the
          path of original `.py`
    Then we expect the following file structure.
    temp-dir
        ├── hello.py      # Python sample test file
        ├── hello.so
    """
    # Given
    sample_files_path = sample_nuitka_build_fixture
    assert len(list(sample_files_path.iterdir())) == 4
    # When
    nuitka_compiler = NuitkaCompiler()
    nuitka_compiler.cleanup(file_path=sample_files_path / "hello.py")
    # Then
    assert len(list(sample_files_path.iterdir())) == 2


@pytest.mark.parametrize("testing_compiler", [NuitkaCompiler, CythonCompiler])
def test_compilers_cleanup_with_non_build_files(
    sample_files_fixture, testing_compiler
):
    """
    Given a path without any  temp builds
    When we call the `cleanup` from the `compilers`
    Then we expect the files as they are.
    """
    # Given
    sample_files_path = sample_files_fixture
    assert len(list(sample_files_path.iterdir())) == 1
    # When
    compiler = testing_compiler()
    compiler.cleanup(file_path=sample_files_path)
    # Then
    assert len(list(sample_files_path.iterdir())) == 1


@pytest.mark.parametrize(
    "testing_compiler,expected_cmd",
    [
        (NuitkaCompiler, CompilerCommands.nuitka),
        (CythonCompiler, CompilerCommands.cython),
    ],
)
def test_compilers_are_instantiated_with_the_right_cmds(
    testing_compiler, expected_cmd
):
    """
    Given a `compiler`
    When I instantiate it
    Then I expect the right `cmd`
    """
    # Given/When
    compiler = testing_compiler()
    # Then
    assert compiler.cmd == expected_cmd


def test_cannot_instantiate_compiler_without_implement_abstract_methods():
    """
    Test cases to verify that each `compiler` should implement
    all the abstract methods.
    """
    with pytest.raises(TypeError):
        Compiler()

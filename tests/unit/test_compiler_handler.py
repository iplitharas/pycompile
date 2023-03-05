"""
Test cases for the `CompilerHandler`
"""
import logging
from unittest.mock import MagicMock, patch

import pytest

from src import CompilerHandler
from tests.fakes import FakeCompiler

MODULE = "src.compiler_handler"


@patch(MODULE + ".run_sub_process")
def test_compiler_handler_start_compiling(
    mocked_run_sub_process, sample_python_file_fixture
):
    """
    Given a `CompilerHandler` instance.
    When we call the `start_compiling` method
    Then we expect the `run_sub_process` to be called
    """
    # Given
    dir_files = dict()
    sample_folder = sample_python_file_fixture
    dir_files[sample_folder] = ["fake_file"]
    fake_compiler = FakeCompiler()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=False,
        keep_builds=True,
    )
    # When
    compiler_handler.start_compiling()
    # Then
    mocked_run_sub_process.assert_called_with(
        files=dir_files[sample_folder], compile_cmd=fake_compiler.cmd
    )


@patch(MODULE + ".run_sub_process")
def test_start_compiling_calls_clean_build_files(
    mocked_run_sub_process, sample_python_file_fixture
):
    """
    Given a `CompilerHandler` instance with `keep_builds=False`,
     When we call the `start_compiling` method
     Then we expect we call the `_clean_build_files` to be called once.
    """
    # Given
    dir_files = dict()
    sample_folder = sample_python_file_fixture
    dir_files[sample_folder] = ["fake_file"]
    fake_compiler = FakeCompiler()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=False,
        keep_builds=False,
    )
    compiler_handler._clean_build_files = MagicMock()
    # When
    compiler_handler.start_compiling()
    # Then
    mocked_run_sub_process.assert_called_with(
        files=dir_files[sample_folder], compile_cmd=fake_compiler.cmd
    )
    compiler_handler._clean_build_files.assert_called_once_with(
        files=dir_files[sample_folder]
    )


@patch(MODULE + ".run_sub_process")
def test_start_compiling_skips_clean_build_files(
    mocked_run_sub_process, sample_python_file_fixture
):
    """
    Given a `CompilerHandler` instance with `keep_builds=True`,
    When we call the `start_compiling` method
    Then we expect to skip the call of the `_clean_build_files`.
    """
    # Given
    dir_files = dict()
    sample_folder = sample_python_file_fixture
    dir_files[sample_folder] = ["fake_file"]
    fake_compiler = FakeCompiler()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=False,
        keep_builds=True,
    )
    compiler_handler._clean_build_files = MagicMock()
    # When
    compiler_handler.start_compiling()
    # Then
    mocked_run_sub_process.assert_called_with(
        files=dir_files[sample_folder], compile_cmd=fake_compiler.cmd
    )
    compiler_handler._clean_build_files.assert_not_called()


@patch(MODULE + ".run_sub_process")
def test_start_compiling_handler_skips_clean_source_files(
    mocked_run_sub_process, sample_python_file_fixture
):
    """
    Given a `CompilerHandler` instance with `clean_source=False`,
    When we call the `start_compiling` method
    Then we expect to skip the call of the `_clean_source_files`.
    """
    # Given
    dir_files = dict()
    sample_folder = sample_python_file_fixture
    dir_files[sample_folder] = ["fake_file"]
    fake_compiler = FakeCompiler()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=False,
        keep_builds=True,
    )
    compiler_handler._clean_source_files = MagicMock()
    # When
    compiler_handler.start_compiling()
    # Then
    mocked_run_sub_process.assert_called_with(
        files=dir_files[sample_folder], compile_cmd=fake_compiler.cmd
    )
    compiler_handler._clean_source_files.assert_not_called()


@patch(MODULE + ".run_sub_process")
def test_start_compiling_handler_calls_clean_source_files(
    mocked_run_sub_process, sample_python_file_fixture
):
    """
    Given a `CompilerHandler` instance with `clean_source=True`,
    When we call the `start_compiling` method
    Then we expect a  call to the `_clean_source_files` method.
    """
    # Given
    dir_files = dict()
    sample_folder = sample_python_file_fixture
    dir_files[sample_folder] = ["fake_file"]
    fake_compiler = FakeCompiler()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=True,
        keep_builds=True,
    )
    compiler_handler._clean_source_files = MagicMock()
    # When
    compiler_handler.start_compiling()
    # Then
    mocked_run_sub_process.assert_called_with(
        files=dir_files[sample_folder], compile_cmd=fake_compiler.cmd
    )
    compiler_handler._clean_source_files.assert_called_with(
        files=dir_files[sample_folder]
    )


def test_clean_source_files(sample_files_fixture, caplog):
    """
    Given a list of file paths
    When we call the `_clean_source_files`
    Then we expect all the files to be deleted and the right
    log message.
    """
    caplog.set_level(logging.WARNING)
    caplog.clear()
    # Given
    dir_files = dict()
    sample_folder = sample_files_fixture
    dir_files["fake_path"] = list(sample_folder.iterdir())
    assert len(dir_files["fake_path"]) == 1
    # When
    fake_compiler = FakeCompiler()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=True,
        keep_builds=True,
    )
    compiler_handler._clean_source_files(files=dir_files["fake_path"])
    # Then
    assert len(list(sample_folder.iterdir())) == 0
    assert "Flag `--clean-source` is on" in caplog.text


def test_clean_build_files(sample_files_fixture, caplog):
    """
    Given a list of file paths
    When we call the `_clean_build_files`
    Then we expect the cleanup method of each compiler to be called
    and the right log message.
    """
    caplog.set_level(logging.WARNING)
    caplog.clear()
    # Given
    dir_files = dict()
    sample_folder = sample_files_fixture
    dir_files["fake_path"] = list(sample_folder.iterdir())
    assert len(dir_files["fake_path"]) == 1
    # When
    fake_compiler = FakeCompiler()
    fake_compiler.cleanup = MagicMock()
    compiler_handler = CompilerHandler(
        files=dir_files,
        compiler=fake_compiler,
        clean_source=True,
        keep_builds=False,
    )
    compiler_handler._clean_build_files(files=dir_files["fake_path"])
    # Then
    assert len(list(sample_folder.iterdir())) == 1
    fake_compiler.cleanup.assert_called_with(
        file_path=dir_files["fake_path"][0]
    )
    assert "-keep-builds` is off" in caplog.text

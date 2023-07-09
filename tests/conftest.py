"""
Common pytest fixtures.
"""
from pathlib import Path

import pytest


@pytest.fixture
def sample_python_file_fixture(tmp_path: Path) -> Path:
    """
    Pytest fixture to create a sample `.py` file and return's
    it's parent folder path.
    """
    # Create a sample folder within the `temp_path`
    sample_folder = tmp_path / "sample"
    sample_folder.mkdir()
    # Create a sample file within the sample folder
    python_file = sample_folder / "hello.py"
    content = r"print('Im a python module')"
    python_file.write_text(content)
    assert len(list(sample_folder.iterdir())) == 1
    assert python_file.read_text() == content
    return sample_folder


@pytest.fixture
def sample_python_file_with_test_fixture(tmp_path: Path) -> Path:
    """
    Pytest fixture to create a sample `.py` file with a corresponding
    and return's test file and return its parent folder path.
    """
    # Create a sample folder within the `temp_path`
    sample_folder = tmp_path / "sample"
    sample_folder.mkdir()
    # Create a sample file within the sample folder
    python_file = sample_folder / "hello.py"
    content = r"print('Im a python module')"
    python_file.write_text(content)
    test_file = sample_folder / "test_hello.py"
    content = r"def test_hello():" r"    assert True"
    test_file.write_text(content)
    return sample_folder


@pytest.fixture
def sample_files_fixture(tmp_path: Path) -> Path:
    """
    Pytest fixture to create sample files.
    """
    # Create a sample folder within the `temp_path`
    sample_folder = tmp_path / "sample"
    sample_folder.mkdir()
    # Create a sample file
    txt_file = sample_folder / "1.txt"
    txt_file.touch()
    txt_file.write_text("some contents here")
    assert len(list(sample_folder.iterdir())) == 1
    return sample_folder


@pytest.fixture
def sample_cython_build_fixture(sample_python_file_fixture: Path) -> Path:
    """
    Pytest fixture to create a sample `cython` build file structure.
      sample_folder
        ├── build         # Cython build temp files
        ├── hello.py      # Python sample test file
        ├── hello.c
        ├── hello.so
    """
    sample_folder_path = sample_python_file_fixture
    assert len(list(sample_folder_path.iterdir())) == 1
    # Create a `.c` file within the dir.
    c_file = sample_folder_path / "hello.c"
    c_file.touch()
    # Create the `.so` file.
    binary_file = sample_folder_path / "hello.so"
    binary_file.touch()
    # Create the `build dir` within  the same dir.
    build_dir_path = sample_folder_path / "build"
    build_dir_path.mkdir(parents=True, exist_ok=False)
    assert len(list(sample_folder_path.iterdir())) == 4
    return sample_folder_path


@pytest.fixture
def sample_nuitka_build_fixture(sample_python_file_fixture: Path) -> Path:
    """
    Pytest fixture to create a sample `cython` build file structure.
      sample_folder
        ├── .build         # Nuitka build temp files
        ├── hello.py       # Python sample test file
        ├── hello.pyi
        ├── hello.so
    """
    sample_folder_path = sample_python_file_fixture
    assert len(list(sample_folder_path.iterdir())) == 1
    # Create a `.pyi` file within the dir.
    pyi_file = sample_folder_path / "hello.pyi"
    pyi_file.touch()
    # Create the `.so` file.
    binary_file = sample_folder_path / "hello.so"
    binary_file.touch()
    # Create the `build dir` within  the same dir.
    build_dir_path = sample_folder_path / "hello.build"
    build_dir_path.mkdir(parents=True, exist_ok=False)
    assert len(list(sample_folder_path.iterdir())) == 4
    return sample_folder_path

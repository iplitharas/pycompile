# pycompile

```python
"""                                        _ _
    _ __  _   _  ___ ___  _ __ ___  _ __ (_) | ___
   | '_ \| | | |/ __/ _ \| '_ ` _ \| '_ \| | |/ _ \
   | |_) | |_| | (_| (_) | | | | | | |_) | | |  __/
   | .__/ \__, |\___\___/|_| |_| |_| .__/|_|_|\___|
   |_|    |___/                    |_|
   
"""
```
A CLI tool for compiling python source code using [Cython](https://cython.org/)  or
[Nuitka](https://nuitka.net/).

![PyPI](https://img.shields.io/pypi/v/pycompile)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pycompile)
![PyPI - License](https://img.shields.io/pypi/l/pycompile)
[![Tests](https://github.com/iplitharas/pycompile/actions/workflows/test.yaml/badge.svg)](https://github.com/iplitharas/pycompile/actions/workflows/test.yaml)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/pycompile)


### Latest docs 📝
[here](https://iplitharas.github.io/pycompile/)

## Table of contents
1. [installation 🔨](#installation)
2. [compile](#compile)
3. [benchmark](#benchmark)
4. [dry run](#dry-run)
5. [Local-development 💻🏭](#local-development)


### Installation 
```bash
pip install pycompile
```

### Compile

```bash
Usage: pycompile compile [OPTIONS]

  Compile the python files using `cython` or `nuitka`.

Options:
  -i, --input-path PATH           Specify the file/folder input path, by
                                  default it will exclude any `test` and
                                  `__init__.py` files  [required]
  -ex, --exclude-glob-paths TEXT  glob files patterns of the files to be
                                  excluded, example: **/ignore_this_module.py
  -v, --verbose                   verbose level
  -e, --engine [cython|nuitka]    CompilerWrapper to be used, defaults to:
                                  `cython`
  -cs, --clean-source             Clean source (.py) files
  -kb, --keep-builds              Keep temporary build files
  -ce, --clean-executables        Clean final executables (.so) files
  --help                          Show this message and exit.
```

```bash
pycompile -i your_python_files --clean-source --engine nuitka 
```


```bash
pycompile compile  -i input_path --engine cython 
```

![cython_compile.gif](data/cython_compile.gif) or 

```bash
pycompile compile -i input_path --engine nuitka
```

After the compilation the `input` dir  will have the following structure.

```text
examples
    ├── fib.py.py                           
    ├── fib.cpython-310-darwin.so                      
    ├── test_fib.py                   
```

### Benchmark

It starts a `memory` and a `cpu` benchmark, starting with 
* `python`,
* `cython` and,
* `nuitka`


```bash
pycompile benchmark -i src/examples -vvv
```

![benchmark_cython_python.gif](data/benchmark_cython_python.gif)


> [!IMPORTANT]
> The python package must have a `test_module.py` because both benchmark types are invoked 
> with `pytest` runs


The following structure is required for the `benchmark` subcommand.

```text
 module
    ├── sample_funcs.py                        # implementation
    ├── main.py                                # entrypoint with a `main` function, during compilation will be excluded
    ├── test_sample_funcs.py                   # test cases
```


### Dry-run 

```bash
pycompile dry_run -i ./src
```

![dry_run.gif](data/dry_run.gif)



### Local-development
For local development run the following command

```bash
make setup-local-dev
```

All available `make` commands
```bash
make help
```




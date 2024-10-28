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

| Syntax               | Description                                               |
|----------------------|-----------------------------------------------------------|
| --input-path PATH    | by default it excludes any `test` and `__init__.py` files |
| --clean-source       | Deletes the sources files.                                |
| --keep-builds        | Keeps the temp build files.                               |
| --clean-executables  | Deletes the shared objects (`.so`) files.                 |
| --engine             | Can be `cython` or `nuitka`.                              |
| --exclude-glob-paths | Glob file patterns for excluding specific files.          |
| --verbose            | Increase log messages.                                    |

```bash
pycompile -i your_python_files --clean-source --engine nuitka 
```

By default, the [Cython](https://cython.org/) is being used as the default
compiler. 

> [!TIP]
> For compiling the `examples` use the following command

```bash
pycompile -i input_path --engine cython 
```
which by default, deletes any temp build files and keeps the source files.

![cython_compile.gif](data/cython_compile.gif) or 
```bash
pycompile -i input_path --engine nuitka
```
![nuitka_compile.gif](data/nuitka_compile.gif)

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




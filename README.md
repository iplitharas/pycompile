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

For compiling the `examples` use the following command:
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


| Syntax                      | Description                                                 |
|-----------------------------|-------------------------------------------------------------|
| --input-path PATH           | by default it excludes any `test` and `__init__.py` files   |
| --engine                    | Can be `cython`, `nuitka`, `all` or `none`.                 |
| --type                      | Can be `memory` , `cpy`, or `both`                          |
| --verbose                   | Increase log messages.                                      |
| --profile_func_pattern TEXT | function name pattern for profiling defaults to `benchmark` |

For running a benchmark on  the `input-path` use the following command:
```bash
pycompile benchmark -i src/examples -vvv
```
which by default will start a `memory` and a `cpu` benchmark, starting with 
`python` and then with `cython` and `nuitka`
> The python package must have a `test_module.py` because both benchmark types are invoked 
> with `pytest` runs

* For **memory profiling** the script will decorate all the functions in `benchmark.py` 
  with the `profile` decorator from `memory-profiler`. This is not optimal memory profiling, 
  because we don't actually `profile` the function itself, instead we profile the `caller` but it's necessary
  if we want to `profile` also the compiled code.
  Use the `profile_func_pattern` to specify the function to be profiled in different module for example 
  if `main` is the entrypoint under `main.py` use `--profile_func_pattern main`.

Hence, the following structure are required for the `benchmark` subcommand.

* For **cpu profiling** the same approached is being used, but instead of decorating the `calling functions` 
  it `decorates` the test cases with the `benchmark` from `pytest-benchmark`.


```text
 module
    ├── sample_funcs.py                        # implementation
    ├── main.py                                # entrypoint with a `main` function, during compilation will be excluded
    ├── test_sample_funcs.py                   # test cases
```

**Memory benchmark** using:`3.10.9 (main, Feb  2 2023, 12:59:36) [Clang 14.0.0 (clang-1400.0.29.202)`
```text
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     7     49.4 MiB     49.4 MiB           1   @profile
     8                                         def samples_benchmark():
     9    127.7 MiB     78.4 MiB           1       sum_of_squares()
    10    166.0 MiB     38.3 MiB           1       harmonic_mean()
    11    166.0 MiB      0.0 MiB           1       fibonacci(30)
    12    204.2 MiB     38.2 MiB           1       sum_numbers()
    13     57.7 MiB   -146.5 MiB           1       sum_strings()
```
```text
46.03s call     test_examples.py::test_examples
```
**Memory benchmark** using [cython](https://cython.org/)
```text
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     7     66.5 MiB     66.5 MiB           1   @profile
     8                                         def samples_benchmark():
     9    103.7 MiB     37.3 MiB           1       sum_of_squares()
    10    102.9 MiB     -0.8 MiB           1       harmonic_mean()
    11    102.9 MiB      0.0 MiB           1       fibonacci(30)
    12    104.9 MiB      2.0 MiB           1       sum_numbers()
    13     65.6 MiB    -39.3 MiB           1       sum_strings()
```
```text
4.33s call     test_examples.py::test_examples
```
**Memory benchmark** using [nuitka](https://nuitka.net/index.html)
```text
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
     7     71.6 MiB     71.6 MiB           1   @profile
     8                                         def samples_benchmark():
     9    148.8 MiB     77.1 MiB           1       sum_of_squares()
    10    186.5 MiB     37.7 MiB           1       harmonic_mean()
    11    186.5 MiB      0.0 MiB           1       fibonacci(30)
    12    225.1 MiB     38.6 MiB           1       sum_numbers()
    13    225.1 MiB      0.0 MiB           1       sum_strings()
```
```text
3.45s call     test_examples.py::test_examples
```

**CPU benchmark** using:`3.10.9 (main, Feb  2 2023, 12:59:36) [Clang 14.0.0 (clang-1400.0.29.202)]`
```text
------------------------------------------- benchmark: 1 tests ------------------------------------------
Name (time in s)        Min     Max    Mean  StdDev  Median     IQR  Outliers     OPS  Rounds  Iterations
---------------------------------------------------------------------------------------------------------
test_examples        3.9257  4.0640  3.9731  0.0605  3.9387  0.0917       1;0  0.2517       5           1
---------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
=================================================================================================================
29.40s call     test_examples.py::test_examples
```

**CPU benchmark** using [cython](https://cython.org/)
```text
Name (time in s)        Min     Max    Mean  StdDev  Median     IQR  Outliers     OPS  Rounds  Iterations
---------------------------------------------------------------------------------------------------------
test_examples        4.4198  4.6645  4.4945  0.1048  4.4340  0.1376       1;0  0.2225       5           1
---------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
===================================================================================================================
31.80s call     test_examples.py::test_examples
```

**CPU benchmark** using [nuitka](https://nuitka.net/index.html)
```text
------------------------------------------- benchmark: 1 tests ------------------------------------------
Name (time in s)        Min     Max    Mean  StdDev  Median     IQR  Outliers     OPS  Rounds  Iterations
---------------------------------------------------------------------------------------------------------
test_examples        3.2931  3.5091  3.4278  0.0972  3.4875  0.1571       1;0  0.2917       5           1
---------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
===================================================================================================================
24.02s call     test_examples.py::test_examples
```


![benchmark_cython_python.gif](data/benchmark_cython_python.gif)


### Dry run 

| Syntax               | Description                                               |
|----------------------|-----------------------------------------------------------|
| --input-path PATH    | by default it excludes any `test` and `__init__.py` files |
| --exclude-glob-paths | Glob file patterns for excluding specific files.          |
| --verbose            | Increase log messages.                                    |

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




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

## Table of contents
1. [Local-development](#local-development)
2. [compile](#compile)
3. [benchmark](#benchmark)
4. [dry run](#dry-run)



### Local-development
For local development run the following command
```bash
make setup-local-dev
```
All available `make` commands
```bash
make help
```

### Compile

| Syntax                | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `--input-path PATH`   | by default it will exclude any `test` and `__init__.py` files |
| `--clean-source`      | Deletes the sources files.                                    |
| `--keep-builds`       | Keeps the temp build files.                                   |
| `--clean-executables` | Deletes the shared objects (`.so`) files.                     |
| `--engine`            | Can be `cython` or `nuitka`.                                  |
| `-exclude-glob-paths` | Glob file patterns for excluding specific files.              |
| `--verbose`           | Increase log messages.                                        |

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


| Syntax                         | Description                                                   |
|--------------------------------|---------------------------------------------------------------|
| `--input-path PATH`            | by default it will exclude any `test` and `__init__.py` files |
| `--engine`                     | Can be `cython`, `nuitka`, `all` or `none`.                   |
| `--type`                       | Can be `memory` , `cpy`, or `both`                            |
| `--verbose`                    | Increase log messages.                                        |
| `---profile_func_pattern TEXT` | function name pattern for profiling defaults to `benchmark`   |

For running a benchmark on  the `examples` use the following command:
```bash
pycompile benchmark -i src/examples -vvv --engine cython
```
which by default will start a `memory` and a `cpu` benchmark, starting with 
`python` and then with `cython` and `nuitka`
> The python package must have a `test_module.py` because both benchmark types are invoked 
> with `pytest` runs

* For **memory profiling** the script will decorate all the functions in `main.py` 
  with the `profile` decorator from `memory-profiler`. This is not optimal memory profiling, 
  because we don't actually `profile` the function itself, instead we profile the `caller` but it's necessary
  if we want to `profile` also the compiled code.

* For **cpu profiling** the same approached is being used, but instead of decorating the `calling functions` 
 it `decorates` the test cases with the `benchmark` from `pytest-benchmark`.

Hence, the following structure are required for the `benchmark` subcommand.

```text
 module
    ├── sample_funcs.py                        # implementation
    ├── main.py                                # entrypoint
    ├── test_sample_funcs.py                   # test cases
```


![benchmark_cython_python.gif](data/benchmark_cython_python.gif)


### Dry run 

| Syntax                | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `--input-path PATH`   | by default it will exclude any `test` and `__init__.py` files |
| `-exclude-glob-paths` | Glob file patterns for excluding specific files.              |
| `--verbose`           | Increase log messages.                                        |

```bash
pycompile dry_run -i ./src
```

![dry_run.gif](data/dry_run.gif)



![PyPI - Implementation](https://img.shields.io/pypi/implementation/pycompile)

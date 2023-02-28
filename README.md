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
A `CLI` tool for compiling python source code.

## Table of contents
1. [Local-development](#local-development)
2. [Usages](#usages)

### Local-development
For local development run the following command
```bash
make setup-local-dev
```
All available `make` commands
```bash
make help
```

## Usages 
By default, the [Cython](https://cython.org/) is being used as the default
compiler. 
For compiling any `python` files use the following command:
which: deletes any temp build files and keeps the source files
```bash
pycompile -i examples
```

[![asciicast](https://asciinema.org/a/QK5h8zR0oW2CGvfJtrmWZ3es0.svg)](https://asciinema.org/a/QK5h8zR0oW2CGvfJtrmWZ3es0)

![basic_usage.png](readme%2Fimages%2Fbasic_usage.png)
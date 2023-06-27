.. pycompile documentation master file, created by
   sphinx-quickstart on Tue Jun 27 13:08:22 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pycompile's docs!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   CLI

Contents
==================

* :ref:`genindex`
* :ref:`modindex`



CLI
==================
1. `compile <#compile>`__
2. `benchmark <#benchmark>`__
3. `dry run <#dry-run>`__


=================
compile
=================

+-------------------+--------------------------------------------------+
| Syntax            | Description                                      |
+===================+==================================================+
| ``--              | by default it excludes any ``test`` and          |
| input-path PATH`` | ``__init__.py`` files                            |
+-------------------+--------------------------------------------------+
| `                 | Deletes the sources files.                       |
| `--clean-source`` |                                                  |
+-------------------+--------------------------------------------------+
| ``--keep-builds`` | Keeps the temp build files.                      |
+-------------------+--------------------------------------------------+
| ``--cl            | Deletes the shared objects (``.so``) files.      |
| ean-executables`` |                                                  |
+-------------------+--------------------------------------------------+
| ``--engine``      | Can be ``cython`` or ``nuitka``.                 |
+-------------------+--------------------------------------------------+
| ``--exc           | Glob file patterns for excluding specific files. |
| lude-glob-paths`` |                                                  |
+-------------------+--------------------------------------------------+
| ``--verbose``     | Increase log messages.                           |
+-------------------+--------------------------------------------------+

.. code:: bash

   pycompile -i your_python_files --clean-source --engine nuitka

By default, the `Cython <https://cython.org/>`__ is being used as the
default compiler.

For compiling the ``examples`` use the following command:

.. code:: bash

   pycompile -i input_path --engine cython

which by default, deletes any temp build files and keeps the source
files.

.. code:: bash

   pycompile -i input_path --engine nuitka




After the compilation the ``input`` dir will have the following
structure.

.. code:: text

   examples
       ├── fib.py.py
       ├── fib.cpython-310-darwin.so
       ├── test_fib.py



Benchmark
~~~~~~~~~

+-----------------------+----------------------------------------------+
| Syntax                | Description                                  |
+=======================+==============================================+
| ``--input-path PATH`` | by default it excludes any ``test`` and      |
|                       | ``__init__.py`` files                        |
+-----------------------+----------------------------------------------+
| ``--engine``          | Can be ``cython``, ``nuitka``, ``all`` or    |
|                       | ``none``.                                    |
+-----------------------+----------------------------------------------+
| ``--type``            | Can be ``memory`` , ``cpy``, or ``both``     |
+-----------------------+----------------------------------------------+
| ``--verbose``         | Increase log messages.                       |
+-----------------------+----------------------------------------------+
| ``--profil            | function name pattern for profiling defaults |
| e_func_pattern TEXT`` | to ``benchmark``                             |
+-----------------------+----------------------------------------------+

For running a benchmark on the ``input-path`` use the following command:

.. code:: bash

   pycompile benchmark -i src/examples -vvv

which by default will start a ``memory`` and a ``cpu`` benchmark,
starting with ``python`` and then with ``cython`` and ``nuitka``
The python package must have a ``test_module.py`` because both benchmark
types are invoked  with ``pytest`` runs

-  For **memory profiling** the script will decorate all the functions
   in ``benchmark.py`` with the ``profile`` decorator from
   ``memory-profiler``. This is not optimal memory profiling, because we
   don’t actually ``profile`` the function itself, instead we profile
   the ``caller`` but it’s necessary if we want to ``profile`` also the
   compiled code. Use the ``profile_func_pattern`` to specify the
   function to be profiled in different module for example if ``main``
   is the entrypoint under ``main.py`` use
   ``--profile_func_pattern main``.

Hence, the following structure are required for the ``benchmark``
subcommand.

-  For **cpu profiling** the same approached is being used, but instead
   of decorating the ``calling functions`` it ``decorates`` the test
   cases with the ``benchmark`` from ``pytest-benchmark``.

.. code:: text

    module
       ├── sample_funcs.py                        # implementation
       ├── main.py                                # entrypoint with a `main` function
       ├── test_sample_funcs.py                   # test cases




Dry run
~~~~~~~

+-------------------+--------------------------------------------------+
| Syntax            | Description                                      |
+===================+==================================================+
| ``--              | by default it excludes any ``test`` and          |
| input-path PATH`` | ``__init__.py`` files                            |
+-------------------+--------------------------------------------------+
| ``--exc           | Glob file patterns for excluding specific files. |
| lude-glob-paths`` |                                                  |
+-------------------+--------------------------------------------------+
| ``--verbose``     | Increase log messages.                           |
+-------------------+--------------------------------------------------+

.. code:: bash

   pycompile dry_run -i ./src







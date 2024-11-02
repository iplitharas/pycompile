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

For running a benchmark on the ``input-path`` use the following command:

.. code:: bash

   pycompile benchmark -i src/examples -vvv




Dry run
~~~~~~~

.. code:: bash

   pycompile dry_run -i ./src







"""
CLI entrypoint.
"""
import logging

import click

from src.cli.benchmark_cmd import benchmark_cmd
from src.cli.compile_cmd import compile_cmd
from src.cli.dry_run_cmd import dry_run_cmd

logger = logging.getLogger(__name__)


@click.group()
def main() -> None:
    r"""
                                          _ _
    _ __  _   _  ___ ___  _ __ ___  _ __ (_) | ___
   | '_ \| | | |/ __/ _ \| '_ ` _ \| '_ \| | |/ _ \
   | |_) | |_| | (_| (_) | | | | | | |_) | | |  __/
   | .__/ \__, |\___\___/|_| |_| |_| .__/|_|_|\___|
   |_|    |___/                    |_|
   """
    pass  # pylint: disable=W0107


main.add_command(compile_cmd)  # type: ignore[attr-defined]
main.add_command(benchmark_cmd)  # type: ignore[attr-defined]
main.add_command(dry_run_cmd)  # type: ignore[attr-defined]

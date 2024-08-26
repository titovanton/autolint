import asyncio

import click

from .core import core_loop
from .load_conf import load_conf


@click.group(invoke_without_command=True)
@click.option(
    '--watch-dir',
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True
    ),
    default=None,
    required=False,
    help=(
        'Directory to watch for changes. Overrides '
        'Config.watch_dir if provided.'
    )
)
def main(watch_dir: click.Path | None = None) -> None:
    asyncio.run(core_loop(load_conf(watch_dir)))

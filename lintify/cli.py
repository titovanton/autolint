import click

from .load_conf import load_conf
from .main import core_loop


@click.group(invoke_without_command=True)
@click.argument('watch_dir', type=click.Path(exists=True))
def main(watch_dir: click.Path) -> None:
    core_loop(str(watch_dir), load_conf())

import click

# from .old import main
from .load_conf import load_conf
from .main import core_loop


@click.group(invoke_without_command=True)
@click.argument('path', type=click.Path(exists=True))
def main(path: click.Path) -> None:
    # main(str(path), load_conf())
    core_loop(str(path), load_conf())

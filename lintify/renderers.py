from dataclasses import asdict
from functools import wraps
from typing import Callable

import click

from .frames import LightFrame, Frame
from .schemas import Config, Theme, OutputQMsg


def pre_renderer(func) -> Callable:

    @wraps(func)
    def wrapper(qmessage: OutputQMsg) -> None:
        text = qmessage.message

        if 'no issues found' in text or not text:
            text = 'Non issues found.'

        output = asdict(qmessage)
        output['message'] = text
        func(OutputQMsg(**output))

    return wrapper


@pre_renderer
def raw_renderer(qmessage: OutputQMsg) -> None:
    click.echo(f'{qmessage.linter}: {qmessage.file_path}')
    click.echo(qmessage.message)
    click.echo()


@pre_renderer
def frame_renderer(qmessage: OutputQMsg) -> None:
    LightFrame(
        title=f'{qmessage.linter}: {qmessage.file_path}',
        body=qmessage.message
    )
    click.echo()


def renderer_dispatcher(
    qmessage: OutputQMsg,
    config: Config
) -> None:
    dispatcher: dict[Theme, Callable[[OutputQMsg], None]] = {
        Theme.RAW: raw_renderer,
        Theme.FRAME: frame_renderer,
    }
    dispatcher[config.theme](qmessage)


def _simple_dispatcher(title: str, body: str, config: Config) -> None:
    click.echo()
    match config.theme:
        case Theme.RAW:
            click.echo(title)
            click.echo(body)
            click.echo()
        case Theme.FRAME:
            Frame(title=title, body=body)
            click.echo()


def greatings(config: Config) -> None:
    title = 'AutoLint started'
    body = repr(config)
    _simple_dispatcher(title, body, config)


def byby(message: str, config: Config) -> None:
    title = 'Bye bye...'
    _simple_dispatcher(title, message, config)

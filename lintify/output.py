import asyncio

from .renderers import renderer_dispatcher
from .schemas import Config, OutputQMsg, STOP_OUTPUT_FLAG


async def output_loot_async(
    _output: asyncio.Queue[OutputQMsg],
    config: Config,
) -> None:
    while True:
        message = await _output.get()
        if message == STOP_OUTPUT_FLAG:
            break
        renderer_dispatcher(message, config)

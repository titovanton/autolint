import asyncio

from .schemas import Config, OutputQMsg
from .utils import (
    key_lock,
    run_subprocess_async,
)


# put it in to the _input queue,
# to stop linter loop
STOP_LINTERS_FLAG = 'stop all linters'


async def run_linter_async(
    linter: str,
    path: str,
    _output: asyncio.Queue
) -> None:
    command = linter.format(path=path).split()
    linter = command[0]
    result = await run_subprocess_async(command)
    message, error = result
    await _output.put(OutputQMsg(
        linter=linter,
        file_path=path,
        message=message,
    ))


async def loop_linters(
    path: str,
    config: Config,
    _output: asyncio.Queue,
):
    linters = config.linters or []

    for linter in linters:
        if isinstance(linter, str):
            await run_linter_async(linter, path, _output)
        else:
            await asyncio.gather(*[
                run_linter_async(_lint, path, _output)
                for _lint in linter
            ], return_exceptions=True)

    await key_lock.unlock(path)


async def run_linters_loop_async(
    fs_queue: asyncio.Queue,
    _output: asyncio.Queue,
    config: Config,
) -> None:
    while True:
        path: str = await fs_queue.get()

        if path == STOP_LINTERS_FLAG:
            break

        # This ensures that the files will be handled
        # by a coroutine (one! per file) concurrently.
        if not await key_lock(path):
            asyncio.create_task(
                loop_linters(path, config, _output)
            )

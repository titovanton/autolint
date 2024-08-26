import asyncio

from .fs import run_fs_observer, stop_fs_observer
from .linters import run_linters_loop_async
from .output import output_loot_async
from .renderers import byby, greatings
from .schemas import Config, OutputQMsg


async def _linters_loop(
    fs_queue: asyncio.Queue,
    _output: asyncio.Queue,
    config: Config,
) -> None:
    while True:
        item = await fs_queue.get()  # blocking if empty
        await _output.put(OutputQMsg(
            linter='test',
            file_path=item,
            message='test',
        ))


async def core_loop(config: Config) -> None:
    greatings(config)

    # for the case you haven't created local config
    if not config.linters:
        byby('No linters specified!', config)
        exit(1)

    # to receive file path from the watchdog
    fs_queue: asyncio.Queue = asyncio.Queue()

    # shared output for all the linters
    _output: asyncio.Queue[OutputQMsg] = asyncio.Queue()

    # running watchdog in a thread
    observer = run_fs_observer(
        config, fs_queue, asyncio.get_event_loop()
    )

    try:
        await asyncio.gather(
            output_loot_async(_output, config),
            run_linters_loop_async(fs_queue, _output, config),
        )
    except asyncio.exceptions.CancelledError:
        byby('^C pressed.', config)

        stop_fs_observer(observer)
        # _output.put(STOP_OUTPUT_FLAG)
        # output_thread.join()

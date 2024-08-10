from queue import Queue
from threading import Thread

from .renderers import renderer_dispatcher
from .schemas import Config, OutputQMsg, STOP_OUTPUT_FLAG


def run_output_loop(
    _output: Queue[OutputQMsg],
    config: Config,
) -> Thread:

    def _loop(
        _output: Queue[OutputQMsg],
        config: Config,
    ) -> None:
        while True:
            message = _output.get()
            if message == STOP_OUTPUT_FLAG:
                break
            renderer_dispatcher(message, config)

    thread = Thread(target=_loop, args=[_output, config])
    thread.start()
    return thread

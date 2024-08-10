from queue import Queue
from threading import Thread

from .schemas import OutputQMsg
from .utils import run_linter


# put it in to the _input queue,
# to stop linter loop
STOP_LINTERS_FLAG = 'stop all linters'


def run_linter_loop(
    linter: str,
    _input: Queue,
    _output: Queue[OutputQMsg],
) -> Thread:

    def _loop(
        linter: str,
        _input: Queue,
        _output: Queue[OutputQMsg],
        stop_flag: str,
    ) -> None:
        while True:
            path = _input.get()

            if path == stop_flag:
                break

            command = [linter, path]
            result = run_linter(command)
            _output.put(OutputQMsg(
                linter=linter,
                file_path=path,
                message=result,
            ))

    thread = Thread(target=_loop, args=[
        linter, _input, _output, STOP_LINTERS_FLAG
    ])
    thread.start()
    return thread

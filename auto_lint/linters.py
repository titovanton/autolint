from queue import Queue
from threading import Thread

from .schemas import OutputQMsg
from .utils import run_linter


# put it in to the _input queue,
# to stop linter loop
STOP_LINTERS_FLAG = 'stop all linters'


def run_linter_loop(
    linter: str,
    _input: Queue[str],
    _output: Queue[OutputQMsg],
) -> Thread:
    """
    Starts a loop that runs a specified linter on input data
    from a queue, and places the results in an output queue.
    The loop runs in a separate thread.

    Args:
        linter (str):
            Command string that must contain the
            `{path}` format parameter.
            Example: `mypy {path}`
        _input (Queue[str]):
            A queue containing input data (file paths
            or stop strings) to be linted.
        _output (Queue[OutputQMsg]):
            A queue where linting results will be placed.

    Returns:
        Thread: The thread in which the linter loop is running.
    """

    def _loop(
        linter: str,
        _input: Queue[str],
        _output: Queue[OutputQMsg],
        stop_flag: str,
    ) -> None:
        while True:
            path: str = _input.get()

            if path == stop_flag:
                break

            command = linter.format(path=path).split()
            _linter = command[0]
            result = run_linter(command)
            _output.put(OutputQMsg(
                linter=_linter,
                file_path=path,
                message=result,
            ))

    thread = Thread(target=_loop, args=[
        linter, _input, _output, STOP_LINTERS_FLAG
    ])
    thread.start()
    return thread

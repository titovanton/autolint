import threading
from queue import Queue

from .fs import run_fs_observer, stop_fs_observer
from .linters import run_linter_loop, STOP_LINTERS_FLAG
from .output import run_output_loop
from .schemas import Config, OutputQMsg, STOP_OUTPUT_FLAG
from .renderers import greatings, byby


def core_loop(path: str, config: Config) -> None:
    greatings(config)

    # for the case you haven't created local config
    if not config.linters:
        byby('No linters specified!', config)
        exit(1)

    # to receive file path from the watchdog
    fs_queue: Queue = Queue()

    # to notify all the linters about a file changed
    # independently
    linter_inputs: dict[str, Queue[str]] = {
        lnt: Queue()
        for lnt in config.linters
    }

    # shared output for all the linters
    _output: Queue[OutputQMsg] = Queue()

    # running watchdog in a thread
    observer = run_fs_observer(path, config, fs_queue)

    # running linters
    linter_threads: tuple[threading.Thread, ...] = tuple([
        run_linter_loop(
            lnt,
            linter_inputs[lnt],
            _output,
        )
        for lnt in config.linters
    ])

    # running view/output layer thread
    output_thread = run_output_loop(_output, config)

    try:
        while True:
            item = fs_queue.get()  # blocking if empty
            for q in linter_inputs.values():
                q.put(item)
    except KeyboardInterrupt:
        byby('^C pressed.', config)

        stop_fs_observer(observer)
        _output.put(STOP_OUTPUT_FLAG)
        for q in linter_inputs.values():
            q.put(STOP_LINTERS_FLAG)

        for thread in linter_threads:
            thread.join()
        output_thread.join()

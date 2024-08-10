from queue import Queue

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from .schemas import Config
from .compat import override


class MyEventHandler(PatternMatchingEventHandler):
    @override
    def __init__(self, fs_q: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fs_q = fs_q

    @override
    def on_modified(self, event):
        self.fs_q.put(event.src_path)


def run_fs_observer(
    path: str,
    config: Config,
    fs_q: Queue
) -> BaseObserver:
    event_handler = MyEventHandler(fs_q, patterns=config.files)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    return observer


def stop_fs_observer(observer: BaseObserver) -> None:
    observer.stop()
    observer.join()

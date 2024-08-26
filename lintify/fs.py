import asyncio

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from .compat import override
from .schemas import Config


class MyEventHandler(PatternMatchingEventHandler):
    @override
    def __init__(
        self,
        fs_q: asyncio.Queue,
        loop: asyncio.AbstractEventLoop,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.fs_q = fs_q
        self.loop = loop

    @override
    def on_modified(self, event):
        # self.fs_q.put(event.src_path)
        asyncio.run_coroutine_threadsafe(
            self.fs_q.put(event.src_path),
            self.loop
        )


def run_fs_observer(
    config: Config,
    fs_q: asyncio.Queue,
    loop: asyncio.AbstractEventLoop,
) -> BaseObserver:
    event_handler = MyEventHandler(
        fs_q=fs_q,
        loop=loop,
        patterns=config.files
    )
    observer = Observer()
    observer.schedule(
        event_handler,
        config.watch_dir,
        recursive=True
    )
    observer.start()

    return observer


def stop_fs_observer(observer: BaseObserver) -> None:
    observer.stop()
    observer.join()

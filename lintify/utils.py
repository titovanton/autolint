import asyncio
import subprocess
from typing import Hashable


def get_stdout_with() -> int:
    result = subprocess.run(
        "stty size | cut -d' ' -f2",
        shell=True,
        capture_output=True,
        text=True
    )

    return int(result.stdout.strip())


def run_linter(command: list[str]) -> str:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


async def run_subprocess_async(
    command: list[str]
) -> tuple[str, str]:
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    return (
        stdout.decode('utf-8').strip(),
        stderr.decode('utf-8').strip()
    )


class AsyncSet:
    def __init__(self):
        self._set = set()
        self._lock = asyncio.Lock()

    async def add(self, item):
        async with self._lock:
            self._set.add(item)

    async def remove(self, item):
        async with self._lock:
            self._set.remove(item)

    async def discard(self, item):
        async with self._lock:
            self._set.discard(item)

    async def contains(self, item):
        async with self._lock:
            return item in self._set

    async def __aiter__(self):
        async with self._lock:
            for item in self._set:
                yield item

    async def len(self):
        async with self._lock:
            return len(self._set)


class KeyLock:
    """
    KeyLock is a singleton class that manages locks on
    unique keys using an asynchronous set. This class
    prevents concurrent operations on the same key by
    ensuring only one coroutine can lock a key at a time.

    Usage:

        # Always returns the same instance
        key_lock = KeyLock()

        key: Hashable = ...

        # Returns False and locks the key
        key_lock(key)

        # Subsequent calls return True while locked
        key_lock(key)

        # Unlocks the key, returns None
        key_lock.unlock(key)
    """

    _in_progress: AsyncSet
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def __init__(self):
        self._in_progress = AsyncSet()

    async def __call__(self, key: Hashable) -> bool:
        _in = await self._in_progress.contains(key)

        if not _in:
            await self._in_progress.add(key)
            return False

        return True

    async def unlock(self, key: Hashable) -> None:
        await self._in_progress.remove(key)


key_lock = KeyLock()

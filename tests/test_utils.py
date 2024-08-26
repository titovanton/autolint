import asyncio

from lintify.utils import AsyncSet, RunSemaphore, run_semaphore

import pytest


async def add_items(async_set: AsyncSet) -> None:
    for i in range(100):
        await async_set.add(i)


async def remove_items(async_set: AsyncSet) -> None:
    for i in range(100):
        await async_set.remove(i)


@pytest.mark.asyncio
async def test_asyncset_race_condition():
    async_set = AsyncSet()

    # Create concurrent tasks for adding and removing items
    await asyncio.gather(
        add_items(async_set),
        remove_items(async_set),
    )

    assert await async_set.len() == 0


@pytest.mark.asyncio
async def test_asyncset_iter():
    async_set = AsyncSet()

    await add_items(async_set)

    assert [i async for i in async_set] == list(range(100))
    assert await async_set.contains(10)


@pytest.mark.asyncio
async def test_run_semaphore():
    obj = RunSemaphore()
    assert obj is run_semaphore

    await run_semaphore.lock(1)
    assert await run_semaphore.is_locked(1)

    await run_semaphore.lock(1)
    assert await run_semaphore.is_locked(1)

    await run_semaphore.lock(2)
    await run_semaphore.unlock(1)
    assert await run_semaphore.is_locked(2)
    assert not await run_semaphore.is_locked(1)

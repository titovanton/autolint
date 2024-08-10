"""
I like to use cool new features of Python. But the
reality leads me to use old versions of Python on
old projects. That for I've decided to provide
backword compatability for oldest Python versions.
"""

import sys


__all__ = [
    'override',
    'batched',
]


if sys.version_info >= (3, 12):
    from typing import override
else:
    def override(func):
        """Dummy override decorator for versions before Python 3.12."""
        return func


if sys.version_info >= (3, 11):
    from itertools import batched
else:
    import itertools
    from typing import Iterable, List, TypeVar, Iterator

    T = TypeVar('T')

    def batched(iterable: Iterable[T], n: int) -> Iterator[List[T]]:
        """
        Breaks an iterable into batches of size `n`.

        :param iterable: The input iterable to batch.
        :param n: The size of each batch.
        :return: An iterator that yields batches as lists.
        """
        it = iter(iterable)
        while True:
            batch = list(itertools.islice(it, n))
            if not batch:
                break
            yield batch

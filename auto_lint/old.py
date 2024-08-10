#!/usr/bin/env python
"""
MAINTAINER Titov Anton <webdev@titovanton.com>

Description:
This module utilizes the watchdog observer
to monitor changes in *.py files.
Invokes flake8 and mypy for the specific *.py file,
where changes were detected.
"""

import re
import signal
import subprocess
import sys
import time
from collections import deque
from itertools import batched
from typing import Callable, Deque

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from .utils import get_stdout_with


class PrintF:
    """
    Print in Frame with fixed size

        PrintF(text)
    """

    vborder: str = '║'
    hborder: str = '═'
    tlcorner: str = '╔'
    trcorner: str = '╗'
    blcorner: str = '╚'
    brcorner: str = '╝'
    header_line: str = '─'

    def __init__(
        self,
        title: str,
        body: str | None = None,
        enumerate_body: bool = True,
        skip_row: Callable = lambda row: False,
    ):
        self.title = title
        self.body = body
        self.enumerate_body = enumerate_body
        self.skip_row = skip_row
        self.stdout_width = get_stdout_with()

        # print on instantiation
        self._render_frame()

    def _parse_body(self) -> Deque[str]:
        """
        Splits self.body into bullet points, enumerates
        each of the bullets if needed, then normalize
        each of the bullets by length. Separate bullets
        by blank line.
        """

        if not self.body:
            return deque()

        def split_string(
            input_string: str,
            max_length: int = self.stdout_width - 20
        ) -> Deque[str]:
            """
            Splits a string into substrings based on the
            specified criteria:
            1) Maximum substring length is not more than
               self.stdout_width characters (can be less
               if needed for points 2 and 3).
            2) The string should not start with punctuation
               or space.
            3) All words in the string should be complete,
               i.e., there should be no word fragments at
               the end or beginning of the string, except
               in the case when a word in the string is
               longer than self.stdout_width characters -
               then it can be moved to another line by
               truncating it.

            :param input_string: The input string
            :param max_length: Maximum length of a substring
            :return: List of substrings
            """

            words = re.findall(r'.+?\s|.+?$', input_string.strip())

            result: Deque[str] = deque()
            current_line = ''
            for word in words:
                _word = word.strip()

                # Check if the word fits into the current line
                if len(current_line) + len(_word) + 1 <= max_length:
                    # If the line is not empty,
                    # add a space before the new word
                    if current_line:
                        current_line += ' '
                    current_line += _word
                else:
                    # Add the current line to the result
                    if current_line:
                        result.append(current_line)

                    if len(_word) > max_length:
                        for batch in batched(_word, max_length):
                            current_line = ''.join(batch)
                            result.append(current_line)

                        # last one batch is incompleted
                        result.pop()
                    else:
                        # Start a new line with the current word
                        current_line = _word

            if current_line:
                # Add the last line to the result
                result.append(current_line)

            if result:
                # break line
                result.append('')

            return result

        # Split body into rows with random length
        splited = self.body.split('\n')
        output: Deque[str] = deque()
        enumerate_body = self.enumerate_body and len(splited) > 1

        # each row is a bullet point
        for num, row in enumerate(splited):
            if self.skip_row(row):
                continue

            # normalize length by splitting bullet into rows
            if row:
                _row = row
                if enumerate_body:
                    _row = f'{num+1}) {row}'
                output += split_string(_row)

        if output:
            # break line between bullets
            output.appendleft('')

        return output

    def _render_frame(self):
        border_width = self.stdout_width - 12
        inner_width = self.stdout_width - 16

        # top border
        print(
            f'{self.tlcorner:>6}'
            f'{self.hborder*border_width:^{border_width}}'
            f'{self.trcorner:<6}'
        )

        # title
        print(
            f'{self.vborder:>6}'
            f'{self.title:^{border_width}}'
            f'{self.vborder:<6}'
        )

        if self.body:
            # header line between title and body
            print(
                f'{self.vborder:>6}'
                f'{self.header_line*inner_width:^{border_width}}'
                f'{self.vborder:<6}'
            )

            # body
            for row in self._parse_body():
                print(
                    f'{self.vborder:>6}  '
                    f'{row:<{inner_width}}'
                    f'  {self.vborder:<6}'
                )

        # bottom border
        print(
            f'{self.blcorner:>6}'
            f'{self.hborder*border_width:^{border_width}}'
            f'{self.brcorner:<6}'
        )


class PrintLF(PrintF):
    """
    Print in Frame with thin borders

        PrintLF(text)
    """

    vborder: str = '│'
    hborder: str = '─'
    tlcorner: str = '┌'
    trcorner: str = '┐'
    blcorner: str = '└'
    brcorner: str = '┘'


def _run_command(command: list[str], config) -> None:

    title = ': '.join(command)

    # let the file system commit changes
    time.sleep(0.2)

    result = subprocess.run(command, stdout=subprocess.PIPE)
    output = result.stdout.decode()

    if 'no issues found' in output or not output:
        output = 'Non issues found.'

    def skip_row(row):
        return all([
            'Found' in row,
            'error' in row,
            'file' in row,
            '(checked' in row,
            'source file' in row,
        ])

    PrintLF(title=title, body=output, skip_row=skip_row)
    print('')


def run_flake_mypy(event, config):
    _run_command(['flake8',  event.src_path], config)
    _run_command(['mypy',  event.src_path], config)


class Watcher:
    def __init__(self, path: str, config) -> None:
        self.path = path
        self.config = config

    def run(self) -> None:
        PrintF(title='** WATCHER IS STARTED **')
        event_handler = PatternMatchingEventHandler(
            patterns=['*.py', '*.pyi']
        )

        def wrapped_handler(event):
            run_flake_mypy(event, self.config)

        event_handler.on_modified = wrapped_handler  # type: ignore
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        self.observer.join()

    def stop(self):
        self.observer.stop()


def signal_handler(sig, frame):
    """
    Graceful exit on signal from Docker
    """
    print('Received SIGTERM, exiting gracefully')
    sys.exit(0)


def main(path: str, config):
    signal.signal(signal.SIGTERM, signal_handler)

    watcher = Watcher(path, config)

    try:
        watcher.run()
    except KeyboardInterrupt:
        print(' pressed.\nBye bye...')
        watcher.stop()


if __name__ == '__main__':
    main('./', {})

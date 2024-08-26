from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class Theme(Enum):
    RAW = 'raw'
    FRAME = 'frame'


class Config(BaseModel):
    """
    This configuration defines a sequence of linter
    commands to be executed on a given codebase.

    - Each command listed as a single string is
      executed sequentially, one after another,
      ensuring that each linter runs only after
      the previous one completes.
    - When a command is specified as a list of
      strings, the commands in that list are
      executed concurrently, meaning they run
      in "parallel", independent of one another.

    This setup allows for a flexible and efficient
    linting process, ensuring both ordered execution
    when needed and faster processing through concurrency
    where applicable.
    """

    theme: Theme
    watch_dir: str
    files: list[str]
    linters: list[str | list[str]] | None


@dataclass(frozen=True, kw_only=True, slots=True)
class OutputQMsg:
    linter: str
    file_path: str
    message: str


STOP_OUTPUT_FLAG = OutputQMsg(
    linter='_',
    file_path='_',
    message='stop infinite loop',
)

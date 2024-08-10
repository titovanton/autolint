from dataclasses import dataclass
from enum import Enum
from typing import Literal

from pydantic import BaseModel


class Theme(Enum):
    RAW = 'raw'
    FRAME = 'frame'


class Config(BaseModel):
    wait_fs: float
    theme: Theme
    files: list[str]
    linters: list[Literal['flake8', 'mypy']]


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

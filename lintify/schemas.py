from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class Theme(Enum):
    RAW = 'raw'
    FRAME = 'frame'


class Config(BaseModel):
    theme: Theme
    files: list[str]
    linters: list[str] | None


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

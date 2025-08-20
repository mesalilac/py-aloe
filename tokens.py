from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    KEY = auto()
    VALUE = auto()
    EQUALS = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str | None
    pos: tuple[int, int]

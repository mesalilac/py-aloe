from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    VALUE = auto()
    EQUALS = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    pos: tuple[int, int]

from dataclasses import dataclass
from enum import Enum, auto

CHAR_COMMENT = "#"
CHAR_EQUALS = "="
CHAR_SECTION_SYMBOL = "$"
CHAR_LEFT_PAREN = "}"
CHAR_RIGHT_PAREN = "{"


class TokenType(Enum):
    KEY = auto()
    VALUE = auto()
    EQUALS = auto()
    COMMENT = auto()
    SECTION_NAME = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    NEWLINE = auto()
    EMPTY_LINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str | None
    pos: tuple[int, int]

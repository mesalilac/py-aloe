from dataclasses import dataclass
from enum import Enum, auto

CHAR_COMMENT = "#"
CHAR_EQUALS = "="
CHAR_SECTION_SYMBOL = "$"
CHAR_CURLY_OPEN = "{"
CHAR_CURLY_CLOSE = "}"


class TokenType(Enum):
    KEY = auto()
    VALUE = auto()
    EQUALS = auto()
    COMMENT = auto()
    SECTION_NAME = auto()
    CURLY_OPEN = auto()
    CURLY_CLOSE = auto()
    NEWLINE = auto()
    BLANK_LINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str | None
    pos: tuple[int, int]

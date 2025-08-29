from dataclasses import dataclass
from enum import Enum, auto

CHAR_COMMENT = "#"
CHAR_EQUALS = "="
CHAR_SECTION_SYMBOL = "$"
CHAR_LEFT_PARN = "}"
CHAR_RIGHT_PARN = "{"


class TokenType(Enum):
    KEY = auto()
    VALUE = auto()
    EQUALS = auto()
    COMMENT = auto()
    SECTION_NAME = auto()
    LEFT_PARN = auto()
    RIGHT_PARN = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: str | None
    pos: tuple[int, int]

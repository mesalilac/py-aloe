from dataclasses import dataclass
from enum import Enum, auto

CHAR_COMMENT = "#"
CHAR_EQUALS = "="
CHAR_SECTION_SYMBOL = "$"
CHAR_LBRACE = "{"
CHAR_RBRACE = "}"


class TokenType(Enum):
    KEY = auto()
    VALUE = auto()
    EQUALS = auto()  # =
    COMMENT = auto()
    SECTION_NAME = auto()
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    NEWLINE = auto()  # \n
    BLANK_LINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str | None
    pos: tuple[int, int]

import py_cfg.symbols as symbols
from dataclasses import dataclass, field
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    EQUALS = auto()  # =
    COMMENT = auto()
    SECTION_SYMBOL = auto()
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    COMMA = auto()
    NEWLINE = auto()  # \n
    BLANK_LINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str | int | float | bool | None
    position: tuple[int, int]


@dataclass
class LexerState:
    line = 1
    column = 1
    index = 0

    def __iter__(self):
        yield self.line
        yield self.column


def lex(text: str) -> list[Token]:
    tokens: list[Token] = []
    state = LexerState()

    return tokens

import symbols
from dataclasses import dataclass, field
from enum import Enum, auto


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
    string_literal: bool = False


@dataclass
class State:
    line = 1
    column = 1

    def into_tuple(self) -> tuple[int, int]:
        return (self.line, self.column)


def lex(text: str) -> list[Token]:
    tokens: list[Token] = []
    state = State()

    def push_token(
        type: TokenType, value: str | None = None, string_literal: bool = False
    ):
        tokens.append(
            Token(
                type=type,
                value=value,
                pos=state.into_tuple(),
                string_literal=string_literal,
            )
        )

    def insert_newline():
        push_token(TokenType.NEWLINE)
        state.line += 1

    for line in text.splitlines():
        line = line.strip()
        state.column = 1

        if line.isspace() or not line:
            push_token(TokenType.BLANK_LINE)
            state.line += 1
            continue

        if line.startswith(symbols.COMMENT):
            comment = line.removeprefix(symbols.COMMENT).strip()
            push_token(TokenType.COMMENT, comment)
            insert_newline()
            continue

        if line.startswith(symbols.SECTION_PREFIX):
            section_name = line.removeprefix(symbols.SECTION_PREFIX).strip()

            if section_name.endswith(symbols.LBRACE):
                section_name = section_name.removesuffix(symbols.LBRACE).strip()
                push_token(TokenType.SECTION_NAME, section_name)
                push_token(TokenType.LBRACE)
            else:
                push_token(TokenType.SECTION_NAME, section_name)

            state.column += len(symbols.SECTION_PREFIX) + len(section_name)
            insert_newline()
            continue

        if line == symbols.RBRACE:
            push_token(TokenType.RBRACE)
            state.column += len(symbols.RBRACE)
            insert_newline()
            continue

        if line == symbols.LBRACE:
            push_token(TokenType.LBRACE)
            state.column += len(symbols.LBRACE)
            insert_newline()
            continue

        if symbols.EQUALS in line:
            key, value = line.split(symbols.EQUALS)

            key = key.strip()
            value = value.strip()
            string_literal = False

            if (
                value.startswith('"')
                and value.endswith('"')
                or value.startswith("'")
                and value.endswith("'")
            ):
                value = value[1:-1]
                string_literal = True

            if key and value:
                state.column += len(key)
                push_token(TokenType.KEY, key)
                push_token(TokenType.EQUALS)
                state.column += len(value)
                push_token(TokenType.VALUE, value, string_literal=string_literal)

        insert_newline()

    push_token(TokenType.EOF)

    return tokens

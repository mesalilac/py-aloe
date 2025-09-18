import py_cfg.symbols as symbols
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TypeAlias

T_TOKEN_VALUE: TypeAlias = str | int | float | bool | None


class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    EQUALS = auto()  # =
    COMMENT = auto()  # '# ...'
    SECTION_PREFIX = auto()
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    COMMA = auto()  # ,
    NEWLINE = auto()  # \n
    BLANK_LINE = auto()
    ILLEGAL = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: T_TOKEN_VALUE
    position: tuple[int, int]


@dataclass
class LexerState:
    line = 1
    column = 1
    index = 0

    def into_tuple(self):
        return (self.line, self.column)


def is_number(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


def lex(text: str) -> list[Token]:
    tokens: list[Token] = []
    state = LexerState()

    def advance(by: int = 1) -> str | None:
        for _ in range(by):
            if state.index >= len(text):
                return None
            ch = text[state.index]
            state.index += 1
            if ch == symbols.NEWLINE:
                state.line += 1
                state.column = 1
            else:
                state.column += 1

        return ch

    def push_token(type: TokenType, value: T_TOKEN_VALUE = None) -> None:
        value = value

        match type:
            case TokenType.EQUALS:
                value = symbols.EQUALS
            case TokenType.SECTION_PREFIX:
                value = symbols.SECTION_PREFIX
            case TokenType.LBRACE:
                value = symbols.LBRACE
            case TokenType.RBRACE:
                value = symbols.RBRACE
            case TokenType.LBRACKET:
                value = symbols.LBRACKET
            case TokenType.RBRACKET:
                value = symbols.RBRACKET
            case TokenType.COMMA:
                value = symbols.COMMA
            case TokenType.NEWLINE:
                value = symbols.NEWLINE

        tokens.append(Token(type=type, value=value, position=state.into_tuple()))

    while state.index < len(text):
        ch = text[state.index]

        if ch == symbols.NEWLINE:
            if tokens and tokens[-1].type == TokenType.NEWLINE:
                push_token(TokenType.BLANK_LINE)
            else:
                push_token(TokenType.NEWLINE)

            advance()
        elif ch.isspace():
            advance()
        elif ch == symbols.COMMA:
            push_token(TokenType.COMMA)
            advance()
        elif ch == symbols.LBRACKET:
            push_token(TokenType.LBRACKET)
            advance()
        elif ch == symbols.RBRACKET:
            push_token(TokenType.RBRACKET)
            advance()
        elif ch == symbols.LBRACE:
            push_token(TokenType.LBRACE)
            advance()
        elif ch == symbols.RBRACE:
            push_token(TokenType.RBRACE)
            advance()
        elif ch == symbols.EQUALS:
            push_token(TokenType.EQUALS)
            advance()
        elif ch == symbols.COMMENT:
            advance()

            if text[state.index].isspace():
                advance()

            buffer = ""

            while state.index < len(text) and text[state.index] != symbols.NEWLINE:
                buffer += text[state.index]
                advance()

            push_token(TokenType.COMMENT, buffer)
        elif ch == symbols.SECTION_PREFIX:
            push_token(TokenType.SECTION_PREFIX)
            advance()
        elif ch.isalpha() or ch == "_":
            buffer = ""

            while state.index < len(text) and (
                text[state.index].isalpha() or text[state.index] == "_"
            ):
                buffer += text[state.index]
                advance()

            if tokens and tokens[-1].type == TokenType.EQUALS:
                if buffer.lower() == "true":
                    push_token(TokenType.BOOLEAN, True)
                elif buffer.lower() == "false":
                    push_token(TokenType.BOOLEAN, False)
                else:
                    push_token(TokenType.STRING, buffer)
            else:
                push_token(TokenType.IDENTIFIER, buffer)
        elif ch.isdigit() or ch == "-":
            buffer = ""

            while state.index < len(text) and (
                text[state.index].isdigit() or text[state.index] in ".-"
            ):
                buffer += text[state.index]
                advance()

            if is_number(buffer):
                push_token(TokenType.NUMBER, int(buffer))
            elif is_float(buffer):
                push_token(TokenType.NUMBER, float(buffer))
            else:
                push_token(TokenType.IDENTIFIER, buffer)
        elif ch == symbols.DOUBLE_QUOTE:
            advance()

            buffer = ""

            while state.index < len(text) and (
                text[state.index] != symbols.DOUBLE_QUOTE
                and text[state.index] != symbols.NEWLINE
            ):
                buffer += text[state.index]
                advance()

            if text[state.index] == symbols.DOUBLE_QUOTE:
                advance()

            push_token(TokenType.STRING, buffer)
        else:
            push_token(TokenType.ILLEGAL, ch)
            advance()

    push_token(TokenType.EOF)

    return tokens

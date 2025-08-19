from dataclasses import dataclass
from tokens import TokenType, Token


@dataclass
class State:
    cursor = 0
    line = 1
    column = 1


@dataclass
class Lexer:
    text: str

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        return tokens

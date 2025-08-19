from dataclasses import dataclass
from tokens import TokenType, Token


@dataclass
class State:
    line = 1
    column = 1

    def get_position(self) -> tuple[int, int]:
        return (self.line, self.column)


@dataclass
class Lexer:
    text: str

    def tokenize(self) -> list[Token]:
        state = State()
        tokens: list[Token] = []

        for line in self.text.splitlines():
            state.column = 1

            print(f"line{state.line, state.column}:", line)

            for char in line:
                print(f"char{state.line, state.column}:", char)
                state.column += 1

            state.line += 1

        return tokens

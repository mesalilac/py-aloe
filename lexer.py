from dataclasses import dataclass, field
from tokens import TokenType, Token


@dataclass
class State:
    line = 1
    column = 1

    def into_tuple(self) -> tuple[int, int]:
        return (self.line, self.column)


@dataclass
class Lexer:
    text: str
    tokens: list[Token] = field(default_factory=list)

    def tokenize(self) -> list[Token]:
        state = State()

        for line in self.text.splitlines():
            state.column = 1

            if line.startswith("#"):
                state.line += 1
                continue

            print(f"line{state.line, state.column}:", line)

            for char in line:
                print(f"char{state.line, state.column}:", char)
                state.column += 1

            state.line += 1

        return self.tokens

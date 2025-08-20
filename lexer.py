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

            if "=" in line:
                key, value = line.split("=")

                key = key.strip()
                value = value.strip()

                if (
                    value.startswith('"')
                    and value.endswith('"')
                    or value.startswith("'")
                    and value.endswith("'")
                ):
                    value = value[1:-1]

                state.column += len(key)
                self.tokens.append(Token(TokenType.IDENTIFIER, key, state.into_tuple()))
                self.tokens.append(Token(TokenType.EQUALS, None, state.into_tuple()))
                state.column += len(value)
                self.tokens.append(Token(TokenType.VALUE, value, state.into_tuple()))

            self.tokens.append(Token(TokenType.NEWLINE, None, state.into_tuple()))
            state.line += 1

        return self.tokens

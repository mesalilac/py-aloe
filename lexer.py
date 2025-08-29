from dataclasses import dataclass, field
from tokens import TokenType, Token, CHAR_COMMENT, CHAR_EQUALS


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
            line = line.strip()
            state.column = 1

            if line.startswith(CHAR_COMMENT):
                comment = line.removeprefix(CHAR_COMMENT).strip()
                self.tokens.append(
                    Token(TokenType.COMMENT, comment, state.into_tuple())
                )
                state.line += 1
                continue

            if CHAR_EQUALS in line:
                key, value = line.split(CHAR_EQUALS)

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
                self.tokens.append(Token(TokenType.KEY, key, state.into_tuple()))
                self.tokens.append(Token(TokenType.EQUALS, None, state.into_tuple()))
                state.column += len(value)
                self.tokens.append(Token(TokenType.VALUE, value, state.into_tuple()))
            else:
                key = line.strip()
                state.column += len(key)

                self.tokens.append(Token(TokenType.KEY, key, state.into_tuple()))

            self.tokens.append(Token(TokenType.NEWLINE, None, state.into_tuple()))
            state.line += 1

        return self.tokens

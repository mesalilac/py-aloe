from dataclasses import dataclass, field
from tokens import (
    TokenType,
    Token,
    CHAR_COMMENT,
    CHAR_EQUALS,
    CHAR_SECTION_SYMBOL,
    CHAR_LEFT_PARN,
    CHAR_RIGHT_PARN,
)


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

        def insert_newline():
            self.tokens.append(Token(TokenType.NEWLINE, None, state.into_tuple()))
            state.line += 1

        for line in self.text.splitlines():
            line = line.strip()
            state.column = 1

            if line.startswith(CHAR_COMMENT):
                comment = line.removeprefix(CHAR_COMMENT).strip()
                self.tokens.append(
                    Token(TokenType.COMMENT, comment, state.into_tuple())
                )
                insert_newline()
                continue

            if line.startswith(CHAR_SECTION_SYMBOL):
                section_name = line.removeprefix(CHAR_SECTION_SYMBOL).strip()
                self.tokens.append(
                    Token(TokenType.SECTION_NAME, section_name, state.into_tuple())
                )
                state.column += len(CHAR_SECTION_SYMBOL) + len(section_name)
                insert_newline()
                continue

            if line == CHAR_LEFT_PARN:
                self.tokens.append(Token(TokenType.LEFT_PARN, None, state.into_tuple()))
                state.column += len(CHAR_LEFT_PARN)
                insert_newline()
                continue

            if line == CHAR_RIGHT_PARN:
                self.tokens.append(
                    Token(TokenType.RIGHT_PARN, None, state.into_tuple())
                )
                state.column += len(CHAR_RIGHT_PARN)
                insert_newline()
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

            insert_newline()

        return self.tokens

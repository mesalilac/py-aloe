from dataclasses import dataclass, field
from tokens import (
    TokenType,
    Token,
    CHAR_COMMENT,
    CHAR_EQUALS,
    CHAR_SECTION_SYMBOL,
    CHAR_LEFT_PAREN,
    CHAR_RIGHT_PAREN,
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

        def push_token(type: TokenType, value: str | None):
            self.tokens.append(Token(type=type, value=value, pos=state.into_tuple()))

        def insert_newline():
            push_token(TokenType.NEWLINE, None)
            state.line += 1

        for line in self.text.splitlines():
            line = line.strip()
            state.column = 1

            if line.isspace() or not line:
                push_token(TokenType.EMPTY_LINE, None)
                state.line += 1
                continue

            if line.startswith(CHAR_COMMENT):
                comment = line.removeprefix(CHAR_COMMENT).strip()
                push_token(TokenType.COMMENT, comment)
                insert_newline()
                continue

            if line.startswith(CHAR_SECTION_SYMBOL):
                section_name = line.removeprefix(CHAR_SECTION_SYMBOL).strip()
                push_token(TokenType.SECTION_NAME, section_name)
                state.column += len(CHAR_SECTION_SYMBOL) + len(section_name)
                insert_newline()
                continue

            if line == CHAR_LEFT_PAREN:
                push_token(TokenType.LEFT_PAREN, None)
                state.column += len(CHAR_LEFT_PAREN)
                insert_newline()
                continue

            if line == CHAR_RIGHT_PAREN:
                push_token(TokenType.RIGHT_PAREN, None)
                state.column += len(CHAR_RIGHT_PAREN)
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
                push_token(TokenType.KEY, key)
                push_token(TokenType.EQUALS, None)
                state.column += len(value)
                push_token(TokenType.VALUE, value)

            insert_newline()

        push_token(TokenType.EOF, None)

        return self.tokens

from dataclasses import dataclass, field
from tokens import (
    TokenType,
    Token,
    CHAR_COMMENT,
    CHAR_EQUALS,
    CHAR_SECTION_SYMBOL,
    CHAR_RBRACE,
    CHAR_LBRACE,
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

        def push_token(type: TokenType, value: str | None = None):
            self.tokens.append(Token(type=type, value=value, pos=state.into_tuple()))

        def insert_newline():
            push_token(TokenType.NEWLINE)
            state.line += 1

        for line in self.text.splitlines():
            line = line.strip()
            state.column = 1

            if line.isspace() or not line:
                push_token(TokenType.BLANK_LINE)
                state.line += 1
                continue

            if line.startswith(CHAR_COMMENT):
                comment = line.removeprefix(CHAR_COMMENT).strip()
                push_token(TokenType.COMMENT, comment)
                insert_newline()
                continue

            if line.startswith(CHAR_SECTION_SYMBOL):
                section_name = line.removeprefix(CHAR_SECTION_SYMBOL).strip()

                if section_name.endswith(CHAR_LBRACE):
                    section_name = section_name.removesuffix(CHAR_LBRACE).strip()
                    push_token(TokenType.SECTION_NAME, section_name)
                    push_token(TokenType.LBRACE)
                else:
                    push_token(TokenType.SECTION_NAME, section_name)

                state.column += len(CHAR_SECTION_SYMBOL) + len(section_name)
                insert_newline()
                continue

            if line == CHAR_RBRACE:
                push_token(TokenType.RBRACE)
                state.column += len(CHAR_RBRACE)
                insert_newline()
                continue

            if line == CHAR_LBRACE:
                push_token(TokenType.LBRACE)
                state.column += len(CHAR_LBRACE)
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
                push_token(TokenType.EQUALS)
                state.column += len(value)
                push_token(TokenType.VALUE, value)

            insert_newline()

        push_token(TokenType.EOF)

        return self.tokens

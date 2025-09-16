from dataclasses import dataclass
from py_cfg.lexer import TokenType, Token
from py_cfg.cst import *


class ParserSyntaxError(Exception):
    def __init__(self, *, text: str, message: str, position: tuple[int, int]):
        self.message: str = message
        self.position: tuple[int, int] = position
        self.source: str = "text"
        self.line: str = ""
        self.line_before: str | None = None
        self.line_after: str | None = None

        lines = text.splitlines()
        line_num, col_num = self.position
        line_index = line_num - 1
        if not (0 <= line_index < len(lines)):
            return
        if line_index > 0:
            self.line_before = lines[line_index - 1]
        self.line = lines[line_index]
        if line_index + 1 < len(lines):
            self.line_after = lines[line_index + 1]

    def __str__(self):
        line, column = self.position

        return f"{self.source}:{line}:{column}: {self.message}"

    def __repr__(self):
        return f"ParserSyntaxError(message: `{self.message}`, position: `{self.position}`,  source: `{self.source}`, line: `{self.line}`, line_before: `{self.line_before}`, line_after: `{self.line_after}`)"

    def print(self):
        line_num, col_num = self.position
        line_index = line_num - 1

        prefix_space = " " * len(str(line_num))
        empty_space = " " * max(col_num - 1, 0)

        def print_line(num: int, content: str | None = None):
            if content is not None:
                print(f" {num} | {content}")
            else:
                print(f" {prefix_space} |")

        print(f" {prefix_space} --> {self.source}:{line_num}:{col_num}")

        if self.line_before:
            print_line(line_index, self.line_before)

        print_line(line_num, self.line)

        print(f" {prefix_space} | {empty_space}^")
        print(f" {prefix_space} | {empty_space}| {self.message}")
        print_line(line_num)

        if self.line_after:
            print_line(line_index + 2, self.line_after)


@dataclass
class ParserState:
    index: int = 0


def parse(text: str, tokens: list[Token]) -> Document:
    items: T_CstItemsList = []

    state = ParserState()
    sections: list[Section] = []

    def is_at_end() -> bool:
        return state.index >= len(tokens)

    def peek(offset: int = 0) -> Token | None:
        idx = state.index + offset

        if not tokens or is_at_end():
            return None

        return tokens[idx]

    def peek_behind(offset: int = 0) -> Token | None:
        idx = state.index - offset

        if not tokens or idx < 0 or is_at_end():
            return None

        return tokens[idx]

    def check(type_: TokenType, offset=0) -> bool:
        tok = peek(offset)

        return tok is not None and tok.type == type_

    def check_behind(type_: TokenType, offset=0) -> bool:
        tok = peek_behind(offset)

        return tok is not None and tok.type == type_

    def current() -> Token | None:
        return None if is_at_end() else tokens[state.index]

    def report_error(message: str, tok: Token | None = None):
        if tok is None:
            tok = current()

        position = tok.position if tok else (1, 1)

        raise ParserSyntaxError(text=text, message=message, position=position)

    def advance(n=1) -> Token | None:
        if state.index < 0 or is_at_end():
            return None

        tok = tokens[state.index]

        state.index += n

        return tok

    while state.index < len(tokens) and tokens[state.index] != TokenType.EOF:
        token = tokens[state.index]

        advance()

    return Document(items)

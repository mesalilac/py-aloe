from dataclasses import dataclass
from py_cfg.lexer import TokenType, Token
from py_cfg.cst import (
    Comment,
    Document,
    Section,
    T_CstItemsList,
    T_ASSIGNMENT_VALUE,
    Assignment,
    Comment,
    BlankLine,
)


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
        if not (0 < line_index < len(lines)):
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


def parse(text: str, tokens: list[Token]) -> Document:
    items: T_CstItemsList = []

    index = 0
    sections: list[Section] = []

    def peek(offset) -> Token | None:
        target = index + offset

        if target < 0 or target >= len(tokens):
            return None

        return tokens[target]

    while index < len(tokens) and tokens[index] != TokenType.EOF:
        cst_items = items if len(sections) == 0 else sections[-1].body_items
        token = tokens[index]

        if token.type == TokenType.KEY:
            equals_token = peek(1)
            value_token = peek(2)

            if not equals_token or equals_token.type != TokenType.EQUALS:
                raise ParserSyntaxError(
                    text=text,
                    message="Missing '=' after key",
                    position=token.pos,
                )

            if not value_token or value_token.type != TokenType.VALUE:
                raise ParserSyntaxError(
                    text=text,
                    message="Missing VALUE after '='",
                    position=token.pos,
                )

            if token.value and value_token.value:
                value: T_ASSIGNMENT_VALUE = value_token.value

                if not value_token.str_literal:
                    if value_token.value.lower() == "true":
                        value = True
                    elif value_token.value.lower() == "false":
                        value = False
                    elif value_token.value.isdigit():
                        value = int(value_token.value)
                    elif (
                        "." in value_token.value
                        and value_token.value.replace(".", "", 1).isdigit()
                    ):
                        value = float(value_token.value)

                assignment = Assignment(token.value, value)
                cst_items.append(assignment)

        if token.type == TokenType.COMMENT:
            comment = Comment(token.value or "")

            cst_items.append(comment)

        if token.type == TokenType.BLANK_LINE:
            blank_line = BlankLine()

            cst_items.append(blank_line)

        if token.type == TokenType.SECTION_NAME and token.value:
            tok1 = peek(1)
            tok2 = peek(2)

            if not (
                (tok1 and tok1.type == TokenType.LBRACE)
                or (
                    tok1
                    and tok1.type == TokenType.NEWLINE
                    and tok2
                    and tok2.type == TokenType.LBRACE
                )
            ):
                raise ParserSyntaxError(
                    text=text,
                    message="Missing '{' after section name",
                    position=token.pos,
                )

            section = Section(token.value, [])

            if tok1 and tok1.type == TokenType.LBRACE:
                section.inline_lbrace = True

            sections.append(section)

        if token.type == TokenType.LBRACE:
            if not sections:
                raise ParserSyntaxError(
                    text=text,
                    message="Unexpected '{' with no open sections",
                    position=token.pos,
                )

        if token.type == TokenType.RBRACE:
            if not sections:
                raise ParserSyntaxError(
                    text=text,
                    message="Unexpected '}' with no open sections",
                    position=token.pos,
                )

            section = sections.pop()

            if sections:
                sections[-1].body_items.append(section)
            else:
                items.append(section)

        index += 1

    return Document(items)

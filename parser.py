from dataclasses import dataclass
from tokens import TokenType, Token


def inspect_text(text: str, message: str, target: tuple[int, int], source="text"):
    lines = text.splitlines()

    line_num, col_num = target
    line_index = line_num - 1
    col_num = min(col_num, len(lines[line_index]) if line_index < len(lines) else 0)

    if not (0 < line_index < len(lines)):
        return

    prefix_space = " " * len(str(line_num))
    empty_space = " " * max(col_num - 1, 0)

    def print_line(num: int, content: str | None = None):
        if content is not None:
            print(f" {num} | {content}")
        else:
            print(f" {prefix_space} |")

    print(f" {prefix_space} --> {source}:{line_num}:{col_num}")

    if line_index > 0:
        print_line(line_index, lines[line_index - 1])

    print_line(line_num, lines[line_index])

    print(f" {prefix_space} | {empty_space}^")
    print(f" {prefix_space} | {empty_space}| {message}")
    print_line(line_num)

    if line_index + 1 < len(lines):
        print_line(line_index + 2, lines[line_index + 1])


class ParserSyntaxError(Exception):
    def __init__(self, text: str, message: str, position: tuple[int, int]):
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
class Parser:
    tokens: list[Token]
    text: str

    def parse(self) -> dict[str, str]:
        result = {}

        index = 0
        sections: list[str] = []

        def peek(offset: int) -> Token | None:
            pos = index + offset
            return self.tokens[pos] if 0 <= pos < len(self.tokens) else None

        while index < len(self.tokens):
            token = self.tokens[index]

            if token.type == TokenType.SECTION_NAME:
                if token.value:
                    sections.append(token.value)
                    next_token = peek(2)
                    if next_token and next_token.type != TokenType.RIGHT_PARN:
                        raise ParserSyntaxError(
                            text=self.text,
                            message="Missing RIGHT_PARN '{' after section",
                            position=equals_token.pos,
                        )
                else:
                    raise ParserSyntaxError(
                        text=self.text,
                        message="Missing section name",
                        position=equals_token.pos,
                    )

            if token.type == TokenType.LEFT_PARN:
                sections.pop()

            if token.type == TokenType.KEY:
                equals_token = peek(1)
                value_token = peek(2)

                if not equals_token or equals_token.type != TokenType.EQUALS:
                    raise ParserSyntaxError(
                        text=self.text,
                        message=f"Missing '=' after Key '{key}'",
                        position=equals_token.pos,
                    )

                    index += 1
                    continue

                if not value_token or value_token.type != TokenType.VALUE:
                    raise ParserSyntaxError(
                        text=self.text,
                        message="Missing value after '='",
                        position=value_token.pos,
                    )
                    index += 1
                    continue

                key = token.value
                value = value_token.value

                if len(sections) > 0:
                    section = result

                    for name in sections:
                        if name not in section:
                            section[name] = {}

                        section = section[name]

                    section[key] = value
                else:
                    result[key] = value

            index += 1

        return result

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


@dataclass
class Parser:
    tokens: list[Token]
    text: str

    def parse(self) -> dict[str, str]:
        result = {}

        index = 0

        def peek(offset: int) -> Token | None:
            pos = index + offset
            return self.tokens[pos] if 0 <= pos < len(self.tokens) else None

        while index < len(self.tokens):
            token = self.tokens[index]

            if token.type == TokenType.IDENTIFIER:
                equals_token = peek(1)
                value_token = peek(2)

                if not equals_token or equals_token.type != TokenType.EQUALS:
                    inspect_text(
                        text=self.text,
                        message="Missing '=' after Key",
                        target=equals_token.pos,
                    )
                    index += 1
                    continue

                if not value_token or value_token.type != TokenType.VALUE:
                    inspect_text(
                        text=self.text,
                        message="Missing value after '='",
                        target=value_token.pos,
                    )
                    index += 1
                    continue

                key = token.value
                value = value_token.value

                result[key] = value

            index += 1

        return result

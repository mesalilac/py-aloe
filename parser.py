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

    def parse(self) -> dict[str, str]:
        result = {}

        return result

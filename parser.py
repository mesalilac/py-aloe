from dataclasses import dataclass
from tokens import TokenType, Token


def inspect_text(text: str, message: str, target: tuple[int, int], source="text"):
    target_line = target[0]
    target_column = target[1]
    line_index = target_line - 1

    lines = text.splitlines()
    empty_space = " " * (target_column - 1)

    try:
        line = lines[line_index]

        print(f"--> {source}:{target_line}:{target_column}")
        print(line)
        print(f"{empty_space}^ {message}")
        print()
    except IndexError:
        pass


@dataclass
class Parser:
    tokens: list[Token]

    def parse(self) -> dict[str, str]:
        result = {}

        return result

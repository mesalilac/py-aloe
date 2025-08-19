from dataclasses import dataclass
from tokens import TokenType, Token


@dataclass
class Parser:
    tokens: list[Token]

    def parse(self) -> dict[str, str]:
        result = {}

        return result

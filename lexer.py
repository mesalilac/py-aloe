from dataclasses import dataclass


@dataclass
class State:
    cursor = 0
    line = 1
    column = 1


@dataclass
class Lexer:
    text: str

    def tokenize(self):
        pass

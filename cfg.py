"""high-level Cfg class"""

from cst import Document
from lexer import Lexer
from parser import Parser, ParserSyntaxError


class Cfg:
    def __init__(self, document: Document, filename: str | None = None):
        self.filename = filename
        self.document = document

    @classmethod
    def from_text(cls, text: str):
        tokens = Lexer(text).tokenize()
        document = Parser().parse(text, tokens)
        return cls(document)

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            text = f.read()

            tokens = Lexer(text).tokenize()
            document = Parser().parse(text, tokens)

            return cls(document)

    def to_text(self) -> str:
        return self.document.to_text()

    def save(self, filename: str | None = None) -> None:
        path = filename if filename else self.filename

        if path is None:
            raise ValueError(
                f"No filename provided: pass a filename or set self.filename by calling Cfg.from_file()"
            )

        with open(path, "w") as f:
            f.write(self.document.to_text())

    def get(self, path: str) -> str | None:
        raise NotImplementedError

    def set(self, path: str, value: str) -> None:
        raise NotImplementedError

    def remove(self, path: str) -> None:
        raise NotImplementedError

"""high-level Cfg class"""

from cst import Document
from lexer import Lexer
from parser import Parser, ParserSyntaxError


class Cfg:
    def __init__(self, document: Document):
        self.document: Document = document

    # TODO: return Document from Parser parse method
    # @classmethod
    # def from_text(cls, text: str) -> Cfg:
    #     tokens = Lexer(text).tokenize()
    #     document = Parser(tokens, text).parse()
    #     return cls(document)

    def to_text(self) -> str:
        raise NotImplementedError

    def get(self, path: str) -> str | None:
        raise NotImplementedError

    def set(self, path: str, value: str) -> None:
        raise NotImplementedError

    def remove(self, path: str) -> None:
        raise NotImplementedError

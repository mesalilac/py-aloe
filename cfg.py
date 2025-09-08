"""high-level Cfg class"""

from cst import Document, Assignment, Section
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

    def save(self, filename: str | None = None) -> None:
        path = filename if filename else self.filename

        if path is None:
            raise ValueError(
                f"No filename provided: pass a filename or set self.filename by calling Cfg.from_file()"
            )

        with open(path, "w") as f:
            f.write(self.document.to_text())

    def get(self, path: str) -> str | None:
        """
        Retrieve the value associated with a key in the Document

        The key can be nested within sections using dot notation

        Example:
            `get("network.port")`
            `network` is the section, `port` is the key
        """
        path_parts = path.split(".")

        current_scope = self.document.items

        for index, part in enumerate(path_parts):
            for node in current_scope:
                is_last_part = index == len(path_parts) - 1

                match node:
                    case Assignment():
                        if is_last_part and node.key == part:
                            return node.value
                    case Section():
                        if is_last_part:
                            return None  # cannot return a section as a value
                        if node.name == part:
                            current_scope = node.body_items

    def set(self, path: str, value: str) -> None:
        raise NotImplementedError

    def remove(self, path: str) -> None:
        raise NotImplementedError

    def clear(self, path: str | None = None) -> None:
        if path is None:
            self.document.items.clear()
            return None

        path_parts = path.split(".")

        current_scope = self.document.items

        for index, part in enumerate(path_parts):
            is_last_part = index == len(path_parts) - 1

            for node in current_scope:
                match node:
                    case Assignment():
                        if is_last_part and node.key == part:
                            node.value = ""
                            return None
                    case Section():
                        if is_last_part:
                            node.body_items.clear()
                            return None
                        if node.name == part:
                            current_scope = node.body_items

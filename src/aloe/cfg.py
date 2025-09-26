"""high-level Cfg class"""

from .ast import (
    Document,
    AssignmentNode,
    SectionNode,
    Null,
    AssignmentValueType,
    DEFAULT_INDENT_STEP,
)
from .lexer import lex
from .parser import parse
from typing import Self


class Cfg:
    """High-level class for parsing

    .. note::
        If the parsing fails a `ParserSyntaxError` error is raised

    Example:

    ```python
    cfg = Cfg.from_file("example.cfg")

    print(cfg.get("network.port"))
    #     ^ 8080

    cfg.set("network.port", "3000")

    print(cfg.get("network.port"))
    #     ^ 3000

    cfg.save("example.cfg")
    ```
    """

    def __init__(self, document: Document, filename: str | None = None):
        self.filename = filename
        self.document = document

    @classmethod
    def from_text(cls, text: str) -> Self:
        tokens = lex(text)
        document = parse("text", text, tokens)
        return cls(document)

    @classmethod
    def from_file(cls, filename: str) -> Self:
        with open(filename, "r") as f:
            text = f.read()

            tokens = lex(text)
            document = parse(filename, text, tokens)

            return cls(document)

    def save(
        self,
        filename: str | None = None,
        compact: bool = False,
        indent_level_step: int = DEFAULT_INDENT_STEP,
    ) -> None:
        path = filename if filename else self.filename

        if path is None:
            raise ValueError(
                "No filename provided: pass a filename or set self.filename by calling Cfg.from_file()"
            )

        with open(path, "w") as f:
            f.write(
                self.document.to_text(
                    compact=compact, indent_level_step=indent_level_step
                )
            )

    def get(self, path: str) -> AssignmentValueType | None:
        """
        Retrieve the value associated with a key in the Document

        The key can be nested within sections using dot notation

        Example:
            `get("network.port")`
            `network` is the section, `port` is the key
        """
        path_parts = path.split(".")

        current_scope = self.document._items

        for index, part in enumerate(path_parts):
            for node in current_scope:
                is_last_part = index == len(path_parts) - 1

                match node:
                    case AssignmentNode():
                        if is_last_part and node.key == part:
                            return node.value
                    case SectionNode():
                        if node.name == part:
                            current_scope = node.body

    def set(self, path: str, value: AssignmentValueType) -> None:
        path_parts = path.split(".")

        current_scope = self.document._items

        for index, part in enumerate(path_parts):
            is_last_part = index == len(path_parts) - 1
            part_found_in_scope: bool = False

            for node in current_scope:
                match node:
                    case AssignmentNode():
                        if is_last_part and node.key == part:
                            part_found_in_scope = True
                            node.value = value
                            return None
                    case SectionNode():
                        if node.name == part:
                            part_found_in_scope = True
                            current_scope = node.body

            if not part_found_in_scope:
                if is_last_part:
                    assignment = AssignmentNode(key=part, value=value)
                    current_scope.append(assignment)
                else:
                    section = SectionNode(name=part, body=[])
                    current_scope.append(section)

                    if isinstance(current_scope[-1], SectionNode):
                        current_scope = current_scope[-1].body

    def remove(self, path: str) -> None:
        path_parts = path.split(".")

        current_scope = self.document._items
        remove_target: int | None = None

        for index, part in enumerate(path_parts):
            is_last_part = index == len(path_parts) - 1

            for node_index, node in enumerate(current_scope):
                match node:
                    case AssignmentNode():
                        if is_last_part and node.key == part:
                            remove_target = node_index
                            break
                    case SectionNode():
                        if node.name == part and is_last_part:
                            remove_target = node_index
                            break
                        elif node.name == part:
                            current_scope = node.body

            if remove_target is not None:
                break

        if remove_target is not None:
            del current_scope[remove_target]

    def clear(self, path: str | None = None) -> None:
        if path is None:
            self.document._items.clear()
            return None

        path_parts = path.split(".")

        current_scope = self.document._items

        for index, part in enumerate(path_parts):
            is_last_part = index == len(path_parts) - 1

            for node in current_scope:
                match node:
                    case AssignmentNode():
                        if is_last_part and node.key == part:
                            node.value = Null
                            return None
                    case SectionNode():
                        if is_last_part:
                            node.body.clear()
                            return None
                        if node.name == part:
                            current_scope = node.body

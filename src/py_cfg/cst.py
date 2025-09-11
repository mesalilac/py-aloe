"""Concrete syntax trees"""

from __future__ import annotations
from typing import TypeAlias
import py_cfg.symbols as symbols

DEFAULT_INDENT = 4

T_ASSIGNMENT_VALUE: TypeAlias = str | int | float | bool


class CstNode:
    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self) -> bool:
        raise NotImplementedError


class Comment(CstNode):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "Comment" + "(" + self.text + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Comment) and self.text == other.text


class Assignment(CstNode):
    def __init__(self, key: str, value: T_ASSIGNMENT_VALUE):
        self.key = key
        self.value = value

    def __str__(self):
        key = self.key
        value = self.value

        return "Assignment" + "(" + f"{key=}, {value=}" + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Assignment)
            and self.key == other.key
            and self.value == other.value
        )


class BlankLine(CstNode):
    def __init__(self):
        pass

    def __str__(self):
        return "BlankLine" + "(" + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, BlankLine)


class Section(CstNode):
    def __init__(
        self,
        name: str,
        body_items: list[Section | Assignment | Comment | BlankLine],
        inline_lbrace: bool = False,
    ):
        self.name = name
        self.inline_lbrace = inline_lbrace
        self.body_items = body_items

    def __str__(self):
        body = ", ".join(map(str, self.body_items))
        return "Section" + "(" + self.name + " " + "{" + body + "}" + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Section)
            and self.name == other.name
            and self.inline_lbrace == other.inline_lbrace
            and self.body_items == other.body_items
        )


T_CstItemsList: TypeAlias = list[Section | Assignment | Comment | BlankLine]


class Document(CstNode):
    def __init__(self, items: T_CstItemsList):
        self.items = items

    def __str__(self):
        return "".join(map(str, self.items))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Document) and self.items == other.items

    def to_text(self) -> str:
        lines: list[str] = []

        def serialize_assignment(node: Assignment, indent_by: int = 0):
            indent = " " * indent_by
            value: str = str(node.value)

            if isinstance(node.value, str):
                value = '"' + value + '"'
            elif isinstance(node.value, bool):
                value = value.lower()

            lines.append(f"{indent}{node.key} {symbols.EQUALS} {value}")

        def serialize_comment(node: Comment, indent_by: int = 0):
            indent = " " * indent_by
            lines.append(f"{indent}{symbols.COMMENT} {node.text}")

        def serialize_blank_line():
            lines.append("")

        def serialize_section(node: Section, indent_by: int = 0):
            indent = " " * indent_by

            header = f"{symbols.SECTION_PREFIX}{node.name}"
            if node.inline_lbrace:
                header += f" {symbols.LBRACE}"

            lines.append(f"{indent}{header}")

            if not node.inline_lbrace:
                lines.append(f"{indent}{symbols.LBRACE}")

            serialize_items(node.body_items, indent_by=(indent_by + DEFAULT_INDENT))

            lines.append(f"{indent}{symbols.RBRACE}")

        def serialize_items(items: T_CstItemsList, indent_by: int = 0):
            for item in items:
                match item:
                    case Assignment():
                        serialize_assignment(item, indent_by=indent_by)
                    case Comment():
                        serialize_comment(item, indent_by=indent_by)
                    case BlankLine():
                        serialize_blank_line()
                    case Section():
                        serialize_section(item, indent_by=indent_by)

        serialize_items(self.items)

        return "\n".join(lines)

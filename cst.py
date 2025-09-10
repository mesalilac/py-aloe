"""Concrete syntax trees"""

from __future__ import annotations
from typing import TypeAlias
import symbols


DEFAULT_INDENT = 4

T_ASSIGNMENT_VALUE: TypeAlias = str | int | float | bool


class CstNode:
    def __str__(self) -> str:
        raise NotImplementedError


class Comment(CstNode):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Comment" + "(" + self.__str__() + ")"


class Assignment(CstNode):
    def __init__(self, key: str, value: T_ASSIGNMENT_VALUE):
        self.key = key
        self.value = value

    def __str__(self):
        key = self.key
        value = self.value

        return f"{key=}, {value=}"

    def __repr__(self):
        return "Assignment" + "(" + self.__str__() + ")"


class BlankLine(CstNode):
    def __init__(self):
        pass

    def __str__(self):
        return ""

    def __repr__(self):
        return "BlankLine" + "(" + self.__str__() + ")"


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
        return self.name + " " + "{" + body + "}"

    def __repr__(self):
        return "Section" + "(" + self.__str__() + ")"


T_CstItemsList: TypeAlias = list[Section | Assignment | Comment | BlankLine]


class Document(CstNode):
    def __init__(self, items: T_CstItemsList):
        self.items = items

    def __str__(self):
        return "".join(map(str, self.items))

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

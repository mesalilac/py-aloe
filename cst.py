"""Concrete syntax trees"""

from __future__ import annotations
from typing import TypeAlias
from tokens import (
    CHAR_SECTION_SYMBOL,
    CHAR_LBRACE,
    CHAR_RBRACE,
    CHAR_COMMENT,
    CHAR_EQUALS,
)

DEFAULT_INDENT = 4


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
    def __init__(self, key: str, value: str):
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
        inlined = " inline" if self.inline_lbrace else ""
        body = "".join(map(str, self.body_items))
        return self.name + inlined + "{" + body + "}"

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
            lines.append(f"{indent}{node.key} {CHAR_EQUALS} {node.value}")

        def serialize_comment(node: Comment, indent_by: int = 0):
            indent = " " * indent_by
            lines.append(f"{indent}{CHAR_COMMENT} {node.text}")

        def serialize_blank_line():
            lines.append("")

        def serialize_section(node: Section, indent_by: int = 0):
            indent = " " * indent_by

            header = f"{CHAR_SECTION_SYMBOL}{node.name}"
            if node.inline_lbrace:
                header += f" {CHAR_LBRACE}"

            lines.append(f"{indent}{header}")

            if not node.inline_lbrace:
                lines.append(f"{indent}{CHAR_LBRACE}")

            serialize_items(node.body_items, indent_by=(indent_by + DEFAULT_INDENT))

            lines.append(f"{indent}{CHAR_RBRACE}")

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

"""Concrete syntax trees"""

from __future__ import annotations

from typing import TypeAlias


class Node:
    def __str__(self) -> str:
        raise NotImplementedError


class Comment(Node):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Comment" + "(" + self.__str__() + ")"


class Assignment(Node):
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __str__(self):
        key = self.key
        value = self.value

        return f"{key=}, {value=}"

    def __repr__(self):
        return "Assignment" + "(" + self.__str__() + ")"


class BlankLine(Node):
    def __init__(self):
        pass

    def __str__(self):
        return ""

    def __repr__(self):
        return "BlankLine" + "(" + self.__str__() + ")"


class Section(Node):
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


class Document(Node):
    def __init__(self, items: T_CstItemsList):
        self.items = items

    def __str__(self):
        return "".join(map(str, self.items))

    def to_text(self) -> str:
        lines: list[str] = []

        # TODO: convert document items into text file

        return "\n".join(lines)

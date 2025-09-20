"""Concrete syntax trees"""

from __future__ import annotations
from typing import SupportsIndex
from dataclasses import dataclass, field
from collections.abc import Iterable

import py_cfg.symbols as symbols
import sys

DEFAULT_INDENT = 4

type CST_ItemType = Section | Assignment | Comment | BlankLine
type ArrayItemType = Value | Comment
type AssignmentValueType = str | int | float | bool | Array


class CstNode:
    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self) -> bool:
        raise NotImplementedError


@dataclass
class Value:
    value: AssignmentValueType


@dataclass
class Array:
    _items: list[ArrayItemType] = field(default_factory=list)

    @classmethod
    def from_iter(cls, iter: Iterable[ArrayItemType | AssignmentValueType], /):
        array: list[ArrayItemType] = []

        for item in iter:
            match item:
                case Comment():
                    array.append(item)
                case Value():
                    array.append(item)
                case _:
                    array.append(Value(item))

        return cls(array)

    def __iter__(self):
        return (i.value for i in self._items if isinstance(i, Value))

    def __str__(self):
        body = ", ".join(map(str, self._items))
        return "Array" + "[" + body + "]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Array) and self._items == other._items

    @property
    def values(self) -> list:
        return [i.value for i in self._items if isinstance(i, Value)]

    def append(self, value: AssignmentValueType, /) -> None:
        self._items.append(Value(value))

    def append_comment(self, text: str, /) -> None:
        self._items.append(Comment(text))

    def strip_comments(self) -> list[Value]:
        return [item for item in self._items if isinstance(item, Value)]

    def pop(self, index: SupportsIndex = -1, /) -> ArrayItemType:
        return self._items.pop(index)

    def index(
        self,
        value: ArrayItemType,
        start: SupportsIndex = 0,
        stop: SupportsIndex = sys.maxsize,
        /,
    ) -> int:
        return self._items.index(value, start, stop)

    def count(self, value: ArrayItemType, /) -> int:
        return self._items.count(value)

    def insert(self, index: SupportsIndex, object: ArrayItemType, /) -> None:
        self._items.insert(index, object)

    def remove(self, value: ArrayItemType, /) -> None:
        self._items.remove(value)


@dataclass
class Comment(CstNode):
    text: str

    def __str__(self):
        return "Comment" + "(" + self.text + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Comment) and self.text == other.text


@dataclass
class Assignment(CstNode):
    key: str
    value: AssignmentValueType

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


@dataclass
class BlankLine(CstNode):
    def __str__(self):
        return "BlankLine" + "(" + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, BlankLine)


@dataclass
class Section(CstNode):
    name: str
    inline_lbrace: bool = True
    body_items: list[CST_ItemType] = field(default_factory=list)

    def __str__(self):
        body = ", ".join(map(str, self.body_items))
        inline_display = "Inline:true " if self.inline_lbrace else "Inline:false "
        return (
            "Section" + "(" + self.name + " " + inline_display + "{" + body + "}" + ")"
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (
            isinstance(other, Section)
            and self.name == other.name
            and self.inline_lbrace == other.inline_lbrace
            and self.body_items == other.body_items
        )


@dataclass
class Document(CstNode):
    items: list[CST_ItemType]

    def __str__(self):
        return "".join(map(str, self.items))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Document) and self.items == other.items

    def to_text(self) -> str:
        lines: list[str] = []

        def serialize_string(s: str) -> str:
            return '"' + s + '"'

        def serialize_boolean(s: str) -> str:
            return s.lower()

        def serialize_assignment(node: Assignment, indent_by: int = 0):
            indent = " " * indent_by
            value: str = str(node.value)
            line = f"{indent}{node.key} {symbols.EQUALS} "

            match node.value:
                case str():
                    lines.append(line + serialize_string(value))
                case bool():
                    lines.append(line + serialize_boolean(value))
                case Array():
                    array_body_indent = " " * (indent_by + DEFAULT_INDENT)
                    arr = node.value

                    lines.append(line + symbols.LBRACKET)

                    for index, item in enumerate(arr._items):
                        header = f"{array_body_indent}"

                        match item:
                            case Value():
                                header += serialize_string(str(item.value))
                            case Comment():
                                header += symbols.COMMENT + " " + item.text

                        if index != len(arr._items) - 1 and not isinstance(
                            item, Comment
                        ):
                            header += ","

                        lines.append(header)

                    lines.append(indent + symbols.RBRACKET)
                case _:
                    lines.append(line + value)

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

        def serialize_items(items: list[CST_ItemType], indent_by: int = 0):
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

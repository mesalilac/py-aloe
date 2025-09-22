"""Concrete syntax trees"""

import py_cfg.symbols as symbols
import sys

from typing import SupportsIndex
from dataclasses import dataclass, field
from collections.abc import Iterable

DEFAULT_INDENT_STEP = 4

type AST_ItemType = SectionNode | AssignmentNode | CommentNode | BlankLineNode
type ArrayItemType = Value | CommentNode
type AssignmentValueType = str | int | float | bool | Array


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
                case CommentNode():
                    array.append(item)
                case Value():
                    array.append(item)
                case _:
                    array.append(Value(item))

        return cls(array)

    def __iter__(self):
        return (i.value for i in self._items if isinstance(i, Value))

    @property
    def values(self) -> list:
        return [i.value for i in self._items if isinstance(i, Value)]

    def append(self, value: AssignmentValueType, /) -> None:
        self._items.append(Value(value))

    def append_comment(self, text: str, /) -> None:
        self._items.append(CommentNode(text))

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
class CommentNode:
    text: str


@dataclass
class AssignmentNode:
    key: str
    value: AssignmentValueType


@dataclass
class BlankLineNode:
    pass


@dataclass
class SectionNode:
    name: str
    inline_lbrace: bool = True
    body: list[AST_ItemType] = field(default_factory=list)


@dataclass
class Document:
    _items: list[AST_ItemType]

    def to_text(
        self, compact: bool = False, indent_level_step: int = DEFAULT_INDENT_STEP
    ) -> str:
        lines: list[str] = []

        def increment_indent(current: int) -> int:
            return current + indent_level_step

        def serialize_string(s: str) -> str:
            return '"' + s + '"'

        def serialize_boolean(s: str) -> str:
            return s.lower()

        def serialize_array(
            *, arr: Array, is_first_arr: bool, is_part_of_body: bool, indent_by: int = 0
        ) -> None:
            indent = " " * indent_by
            array_body_indent = " " * increment_indent(indent_by)

            if not is_first_arr:
                lines.append(indent + symbols.LBRACKET)

            for index, item in enumerate(arr._items):
                header = ""

                match item:
                    case Value():
                        match item.value:
                            case Array():
                                serialize_array(
                                    arr=item.value,
                                    is_first_arr=False,
                                    is_part_of_body=(
                                        True if index != len(arr._items) - 1 else False
                                    ),
                                    indent_by=increment_indent(indent_by),
                                )
                            case str():
                                header += serialize_string(str(item.value))
                            case bool():
                                header += serialize_boolean(str(item.value))
                            case _:
                                header += str(item.value)
                    case CommentNode():
                        header += symbols.COMMENT + " " + item.text

                if header:
                    if index != len(arr._items) - 1 and not isinstance(
                        item, CommentNode
                    ):
                        header += ","

                    lines.append(array_body_indent + header)

            close_array_line = indent + symbols.RBRACKET

            if is_part_of_body:
                close_array_line += symbols.COMMA

            lines.append(close_array_line)

        def serialize_assignment(node: AssignmentNode, indent_by: int = 0):
            indent = " " * indent_by
            value: str = str(node.value)
            line = f"{indent}{node.key} {symbols.EQUALS} "

            match node.value:
                case str():
                    lines.append(line + serialize_string(value))
                case bool():
                    lines.append(line + serialize_boolean(value))
                case Array():
                    arr = node.value

                    lines.append(line + symbols.LBRACKET)

                    serialize_array(
                        arr=arr,
                        is_first_arr=True,
                        is_part_of_body=False,
                        indent_by=indent_by,
                    )
                case _:
                    lines.append(line + value)

        def serialize_comment(node: CommentNode, indent_by: int = 0):
            indent = " " * indent_by
            lines.append(f"{indent}{symbols.COMMENT} {node.text}")

        def serialize_blank_line():
            if not compact:
                lines.append("")

        def serialize_section(node: SectionNode, indent_by: int = 0):
            indent = " " * indent_by

            header = f"{symbols.SECTION_PREFIX}{node.name}"
            if node.inline_lbrace or compact:
                header += f" {symbols.LBRACE}"

            lines.append(f"{indent}{header}")

            if not node.inline_lbrace and not compact:
                lines.append(f"{indent}{symbols.LBRACE}")

            serialize_items(node.body, indent_by=increment_indent(indent_by))

            lines.append(f"{indent}{symbols.RBRACE}")

        def serialize_items(items: list[AST_ItemType], indent_by: int = 0):
            for item in items:
                match item:
                    case AssignmentNode():
                        serialize_assignment(item, indent_by=indent_by)
                    case CommentNode():
                        serialize_comment(item, indent_by=indent_by)
                    case BlankLineNode():
                        serialize_blank_line()
                    case SectionNode():
                        serialize_section(item, indent_by=indent_by)

        serialize_items(self._items)

        return "\n".join(lines)

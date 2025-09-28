"""Concrete syntax trees"""

import aloe.symbols as symbols
import sys

from typing import SupportsIndex
from dataclasses import dataclass, field
from collections.abc import Iterable
from typing import Self
from io import StringIO

EOL = symbols.NEWLINE
DEFAULT_INDENT_STEP = 4

type AST_ItemType = SectionNode | AssignmentNode | CommentNode | BlankLineNode
type ArrayItemType = Value | CommentNode
type AssignmentValueType = str | int | float | bool | Array | _NullType


@dataclass
class _NullType:
    def __repr__(self):
        return "Null"


Null = _NullType()


@dataclass
class Value:
    value: AssignmentValueType


@dataclass
class Array:
    _items: list[ArrayItemType] = field(default_factory=list)

    @classmethod
    def from_iter(cls, iter: Iterable[ArrayItemType | AssignmentValueType], /) -> Self:
        array: list[ArrayItemType] = []

        for item in iter:
            match item:
                case CommentNode() | Value():
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
        text = DocumentSerializer(self._items, compact, indent_level_step).serialize()

        return text


@dataclass
class DocumentSerializer:
    root: list[AST_ItemType]
    compact: bool
    indent_level_step: int
    out: StringIO = field(default_factory=StringIO)

    def _indent_step(self, level) -> int:
        return level + self.indent_level_step

    @staticmethod
    def _helper_serialize_string(s: str) -> str:
        return f'"{s}"'

    @staticmethod
    def _helper_serialize_boolean(b: bool) -> str:
        return str(b).lower()

    def _helper_serialize_value(
        self, value: AssignmentValueType, indent_by: int = 0
    ) -> None:
        match value:
            case str():
                self.out.write(self._helper_serialize_string(value))
            case bool():
                self.out.write(self._helper_serialize_boolean(value))
            case _NullType():
                self.out.write("null")
            case Array():
                self._helper_serialize_array(value, indent_by)
            case _:
                self.out.write(str(value))

    def _helper_serialize_array(self, arr: Array, indent_by: int = 0) -> None:
        expanded = (
            any(isinstance(item, CommentNode) for item in arr._items)
            or len(arr._items) > 10
        )
        indent_by_body: int = self._indent_step(indent_by)
        indentation = " " * indent_by
        indentation_body = " " * indent_by_body

        if self.compact:
            expanded = False
            arr._items = [item for item in arr._items if isinstance(item, Value)]

        self.out.write(symbols.LBRACKET)
        if expanded:
            self.out.write(EOL)

        for index, item in enumerate(arr._items):
            match item:
                case CommentNode():
                    self._helper_serialize_comment(item, indent_by_body)
                case Value():
                    value = item.value
                    if expanded:
                        self.out.write(indentation_body)
                    self._helper_serialize_value(value, indent_by_body)

            if index != len(arr._items) - 1 and not isinstance(item, CommentNode):
                self.out.write(symbols.COMMA)
                if expanded:
                    self.out.write(EOL)
                else:
                    self.out.write(" ")

        if expanded:
            self.out.write(EOL)
            self.out.write(indentation)
        self.out.write(symbols.RBRACKET)

    def _helper_serialize_assignment(
        self, node: AssignmentNode, indent_by: int = 0
    ) -> None:
        indentation = " " * indent_by

        self.out.write(indentation)
        self.out.write(f"{node.key} = ")

        self._helper_serialize_value(node.value, indent_by)

        self.out.write(EOL)

    def _helper_serialize_comment(self, node: CommentNode, indent_by: int = 0) -> None:
        indentation = " " * indent_by

        self.out.write(indentation)
        self.out.write(f"{symbols.COMMENT} {node.text}")
        self.out.write(EOL)

    def _helper_serialize_blank_line(self) -> None:
        if not self.compact:
            self.out.write(EOL)

    def _helper_serialize_section(self, node: SectionNode, indent_by: int = 0) -> None:
        indent_by_body: int = self._indent_step(indent_by)
        indentation = " " * indent_by

        self.out.write(indentation)
        self.out.write(symbols.SECTION_PREFIX)
        self.out.write(node.name)

        if node.inline_lbrace or self.compact:
            self.out.write(" ")
            self.out.write(symbols.LBRACE)
            self.out.write(EOL)
        else:
            self.out.write(EOL)
            self.out.write(indentation)
            self.out.write(symbols.LBRACE)
            self.out.write(EOL)

        self._helper_serialize_items(node.body, indent_by_body)

        if self.out.getvalue()[-1] != EOL:
            self.out.write(EOL)
        self.out.write(indentation)
        self.out.write(symbols.RBRACE)

    def _helper_serialize_items(
        self, items: list[AST_ItemType], indent_by: int = 0
    ) -> None:
        for item in items:
            match item:
                case SectionNode():
                    self._helper_serialize_section(item, indent_by)
                case CommentNode():
                    self._helper_serialize_comment(item, indent_by)
                case BlankLineNode():
                    self._helper_serialize_blank_line()
                case AssignmentNode():
                    self._helper_serialize_assignment(item, indent_by)

    def serialize(self) -> str:
        self._helper_serialize_items(self.root, 0)

        return self.out.getvalue()

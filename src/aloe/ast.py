"""Concrete syntax trees"""

import aloe.symbols as symbols
import sys

from typing import SupportsIndex
from dataclasses import dataclass, field
from collections.abc import Iterable
from typing import Self
from io import StringIO

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
        out = StringIO()

        return out.getvalue()

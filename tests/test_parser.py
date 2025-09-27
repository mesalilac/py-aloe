import pytest

from aloe.lexer import lex
from aloe.parser import parse, ParserSyntaxError
from aloe.ast import (
    Document,
    AssignmentNode,
    Array,
    CommentNode,
    SectionNode,
    BlankLineNode,
    Null,
)


def test_parse_key_value():
    text = """app_name = "myapp"
    """

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document([AssignmentNode(key="app_name", value="myapp")])

    assert document._items == expected_document._items


def test_parse_key_value_null():
    text = "app_name = NULL"

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document([AssignmentNode(key="app_name", value=Null)])

    assert document._items == expected_document._items


def test_parse_key_value_array():
    text = "array = [1, 2, 3, 4, 5]"

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            AssignmentNode(
                key="array",
                value=Array.from_iter([1, 2, 3, 4, 5]),
            )
        ]
    )

    assert document._items == expected_document._items


def test_parse_key_value_array_null():
    text = "array = [null, null, null, null, null]"

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            AssignmentNode(
                key="array",
                value=Array.from_iter([Null, Null, Null, Null, Null]),
            )
        ]
    )

    assert document._items == expected_document._items


def test_parse_key_value_nested_array():
    text = (
        "array = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4, [1, 2, 3, 4]]]"
    )

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            AssignmentNode(
                key="array",
                value=Array.from_iter(
                    [
                        Array.from_iter([1, 2, 3, 4]),
                        Array.from_iter([1, 2, 3, 4]),
                        Array.from_iter([1, 2, 3, 4]),
                        Array.from_iter(
                            [
                                1,
                                2,
                                3,
                                4,
                                Array.from_iter([1, 2, 3, 4]),
                            ]
                        ),
                    ]
                ),
            )
        ]
    )

    assert document._items == expected_document._items


def test_parse_section():
    text = """# global settings

    @feature_flags {
        enable_experimental = true
        use_cache = false
    }"""

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            CommentNode("global settings"),
            BlankLineNode(),
            SectionNode(
                name="feature_flags",
                body=[
                    AssignmentNode(key="enable_experimental", value=True),
                    AssignmentNode(key="use_cache", value=False),
                ],
                inline_lbrace=True,
            ),
        ]
    )

    assert document._items == expected_document._items


def test_parse_nested_section():
    text = """# global settings

    @database
    {
        host = "localhost"
        port = 5432
        user = "admin"
        password = "secret"

        @pool {
            max_connections = 20
            timeout = 30
        }
    }"""

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            CommentNode("global settings"),
            BlankLineNode(),
            SectionNode(
                name="database",
                body=[
                    AssignmentNode(key="host", value="localhost"),
                    AssignmentNode(key="port", value=5432),
                    AssignmentNode(key="user", value="admin"),
                    AssignmentNode(key="password", value="secret"),
                    BlankLineNode(),
                    SectionNode(
                        name="pool",
                        body=[
                            AssignmentNode(key="max_connections", value=20),
                            AssignmentNode(key="timeout", value=30),
                        ],
                        inline_lbrace=True,
                    ),
                ],
                inline_lbrace=False,
            ),
        ]
    )

    assert document._items == expected_document._items


def test_to_text():
    text = """# global settings
app_name = "myapp"
version = null
array = ["package-1", "package-2", "package-3", "package-4", "package-5"]
array_with_comments = [
    "package-1",
    "package-2",
    # "package-3",
    "package-4",
    ["package-1", "package-2", "package-3", "package-4", "package-5"],
    [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15
    ]
]

@database
{
    host = "localhost"
    port = 5432
    user = "admin"
    password = "secret"

    @pool {
        max_connections = 20
        timeout = 30
    }
}"""

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_text = text

    assert document.to_text() == expected_text


def test_syntax_error_missing_section_name():
    text = """# global settings

    {
        enable_experimental = true
        use_cache = false
    }"""

    tokens = lex(text)

    with pytest.raises(ParserSyntaxError):
        parse("text", text, tokens)


def test_syntax_error_missing_section_symbol():
    text = """# global settings

    feature_flags {
        enable_experimental = true
        use_cache = false
    }"""

    tokens = lex(text)

    with pytest.raises(ParserSyntaxError):
        parse("text", text, tokens)


# def test_syntax_error_missing_section_LBRACE():
#     text = """# global settings

#     @feature_flags
#         enable_experimental = true
#         use_cache = false
#     }"""

#     tokens = lex(text)

#     with pytest.raises(ParserSyntaxError):
#         parse("text", text, tokens)

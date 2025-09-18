import pytest

from py_cfg.lexer import lex
from py_cfg.parser import *


def test_parse_key_value():
    text = "app_name = myapp"

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document([Assignment(key="app_name", value="myapp")])

    assert document.items == expected_document.items


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
            Comment("global settings"),
            BlankLine(),
            Section(
                name="feature_flags",
                body_items=[
                    Assignment(key="enable_experimental", value=True),
                    Assignment(key="use_cache", value=False),
                ],
                inline_lbrace=True,
            ),
        ]
    )

    assert document.items == expected_document.items


def test_parse_nested_section():
    text = """# global settings

    @database
    {
        host = localhost
        port = 5432
        user = admin
        password = secret

        @pool {
            max_connections = 20
            timeout = 30
        }
    }"""

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            Comment("global settings"),
            BlankLine(),
            Section(
                name="database",
                body_items=[
                    Assignment(key="host", value="localhost"),
                    Assignment(key="port", value=5432),
                    Assignment(key="user", value="admin"),
                    Assignment(key="password", value="secret"),
                    BlankLine(),
                    Section(
                        name="pool",
                        body_items=[
                            Assignment(key="max_connections", value=20),
                            Assignment(key="timeout", value=30),
                        ],
                        inline_lbrace=True,
                    ),
                ],
                inline_lbrace=False,
            ),
        ]
    )

    assert document.items == expected_document.items


def test_to_text():
    text = """# global settings
    app_name = myapp

    @database
    {
        host = localhost
        port = 5432
        user = admin
        password = secret

        @pool {
            max_connections = 20
            timeout = 30
        }
    }"""

    tokens = lex(text)
    document = parse("text", text, tokens)

    expected_document = Document(
        [
            Comment("global settings"),
            Assignment(key="app_name", value="myapp"),
            BlankLine(),
            Section(
                name="database",
                body_items=[
                    Assignment(key="host", value="localhost"),
                    Assignment(key="port", value=5432),
                    Assignment(key="user", value="admin"),
                    Assignment(key="password", value="secret"),
                    BlankLine(),
                    Section(
                        name="pool",
                        body_items=[
                            Assignment(key="max_connections", value=20),
                            Assignment(key="timeout", value=30),
                        ],
                        inline_lbrace=True,
                    ),
                ],
                inline_lbrace=False,
            ),
        ]
    )

    assert document.to_text() == expected_document.to_text()


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

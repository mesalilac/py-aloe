from aloe.lexer import lex
from aloe.lexer import TokenType as Type


def build_simple_line(*args):
    return (*args, Type.NEWLINE)


def build_key_value_pair(*value) -> tuple[Type, Type, Type, Type]:
    return (Type.IDENTIFIER, Type.EQUALS, *value, Type.NEWLINE)


def build_section(*args):
    return (
        Type.SECTION_PREFIX,
        Type.IDENTIFIER,
        Type.LBRACE,
        Type.NEWLINE,
        *args,
        Type.RBRACE,
        Type.NEWLINE,
    )


def test_lex_key_value_string():
    text = """app_name = "myapp"
    """

    tokens = [t.type for t in lex(text)]

    expected = [*build_key_value_pair(Type.STRING), Type.EOF]

    assert tokens == expected


def test_lex_key_value_number():
    text = """max_connections = 20 
    """

    tokens = [t.type for t in lex(text)]

    expected = [*build_key_value_pair(Type.NUMBER), Type.EOF]

    assert tokens == expected


def test_lex_key_value_boolean():
    text = """active = true 
    """

    tokens = [t.type for t in lex(text)]

    expected = [*build_key_value_pair(Type.BOOLEAN), Type.EOF]

    assert tokens == expected


def test_lex_key_value_null():
    text = """name = null
    """

    tokens = [t.type for t in lex(text)]

    expected = [*build_key_value_pair(Type.NULL), Type.EOF]

    assert tokens == expected


def test_lex_key_value_array():
    text = """array = ["string-1", "string-2", "string-3", "string-4"]
    """

    tokens = [t.type for t in lex(text)]

    expected = [
        *build_key_value_pair(
            Type.LBRACKET,
            *(
                Type.STRING,
                Type.COMMA,
                Type.STRING,
                Type.COMMA,
                Type.STRING,
                Type.COMMA,
                Type.STRING,
            ),
            Type.RBRACKET,
        ),
        Type.EOF,
    ]

    assert tokens == expected


def test_lex_key_value_nested_array():
    text = """array = [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4, [1, 2, 3, 4]]]
    """

    tokens = [t.type for t in lex(text)]

    expected = [
        *build_key_value_pair(
            Type.LBRACKET,
            *(
                Type.LBRACKET,
                *(
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                ),
                Type.RBRACKET,
                Type.COMMA,
                Type.LBRACKET,
                *(
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                ),
                Type.RBRACKET,
                Type.COMMA,
                Type.LBRACKET,
                *(
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                ),
                Type.RBRACKET,
                Type.COMMA,
                Type.LBRACKET,
                *(
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.NUMBER,
                    Type.COMMA,
                    Type.LBRACKET,
                    *(
                        Type.NUMBER,
                        Type.COMMA,
                        Type.NUMBER,
                        Type.COMMA,
                        Type.NUMBER,
                        Type.COMMA,
                        Type.NUMBER,
                    ),
                    Type.RBRACKET,
                ),
                Type.RBRACKET,
            ),
            Type.RBRACKET,
        ),
        Type.EOF,
    ]

    assert tokens == expected


def test_lex_key_value_empty_value():
    text = "app_name ="

    tokens = [t.type for t in lex(text)]

    expected = [Type.IDENTIFIER, Type.EQUALS, Type.EOF]

    assert tokens == expected


def test_lex_key_value_empty_key():
    text = """= "myapp"
    """

    tokens = [t.type for t in lex(text)]

    expected = [Type.EQUALS, Type.STRING, Type.NEWLINE, Type.EOF]

    assert tokens == expected


def test_lex_key_value_empty_key_value():
    text = "="

    tokens = [t.type for t in lex(text)]

    expected = [Type.EQUALS, Type.EOF]

    assert tokens == expected


def test_lex_key_value_with_comment():
    text = """# global settings
    
    app_name = "myapp"
    """

    tokens = [t.type for t in lex(text)]

    expected = [
        *build_simple_line(Type.COMMENT),
        Type.BLANK_LINE,
        *build_key_value_pair(Type.STRING),
        Type.EOF,
    ]

    assert tokens == expected


def test_lex_section():
    text = """@feature_flags {
        enable_experimental = true
        use_cache = false
    }
    """

    tokens = [t.type for t in lex(text)]

    expected = [
        *build_section(
            *build_key_value_pair(Type.BOOLEAN),
            *build_key_value_pair(Type.BOOLEAN),
        ),
        Type.EOF,
    ]

    assert tokens == expected


def test_lex_nested_section():
    text = """@database {
        host = "localhost"
        port = 5432
        user = "admin"
        password = "secret"

        @pool {
            max_connections = 20
            timeout = 30
        }
    }
"""

    tokens = [t.type for t in lex(text)]

    expected = [
        *build_section(
            *build_key_value_pair(Type.STRING),
            *build_key_value_pair(Type.NUMBER),
            *build_key_value_pair(Type.STRING),
            *build_key_value_pair(Type.STRING),
            Type.BLANK_LINE,
            *build_section(
                *build_key_value_pair(Type.NUMBER),
                *build_key_value_pair(Type.NUMBER),
            ),
        ),
        Type.EOF,
    ]

    assert tokens == expected

from py_cfg.lexer import lex, TokenType


def test_lex_key_value():
    text = "app_name = myapp"

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.KEY,
        TokenType.EQUALS,
        TokenType.VALUE,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert tokens == expected


def test_lex_key_value_empty_value():
    text = "app_name ="

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.KEY,
        TokenType.EQUALS,
        TokenType.VALUE,
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert tokens == expected


def test_lex_key_value_empty_key():
    text = "= myapp"

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert tokens == expected


def test_lex_key_value_empty_key_value():
    text = "="

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.NEWLINE,
        TokenType.EOF,
    ]

    assert tokens == expected


def test_lex_key_value_with_comment():
    text = """# global settings
    
    app_name = myapp"""

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.COMMENT,
        TokenType.NEWLINE,
        TokenType.BLANK_LINE,
        *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
        TokenType.EOF,
    ]

    assert tokens == expected


def test_lex_section():
    text = """# global settings
    
    @feature_flags {
        enable_experimental = true
        use_cache = false
    }"""

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.COMMENT,
        TokenType.NEWLINE,
        TokenType.BLANK_LINE,
        *(
            TokenType.SECTION_NAME,
            TokenType.LBRACE,
            TokenType.NEWLINE,
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            TokenType.RBRACE,
            TokenType.NEWLINE,
        ),
        TokenType.EOF,
    ]

    assert tokens == expected


def test_lex_nested_section():
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

    tokens = [t.type for t in lex(text)]

    expected = [
        TokenType.COMMENT,
        TokenType.NEWLINE,
        TokenType.BLANK_LINE,
        *(
            TokenType.SECTION_NAME,
            TokenType.NEWLINE,
            TokenType.LBRACE,
            TokenType.NEWLINE,
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            TokenType.BLANK_LINE,
            *(
                TokenType.SECTION_NAME,
                TokenType.LBRACE,
                TokenType.NEWLINE,
                *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
                *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
                TokenType.RBRACE,
                TokenType.NEWLINE,
            ),
            TokenType.RBRACE,
            TokenType.NEWLINE,
        ),
        TokenType.EOF,
    ]

    assert tokens == expected

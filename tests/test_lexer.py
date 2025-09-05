import unittest
from lexer import Lexer
from tokens import Token, TokenType

KV_PAIR = (TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEW_LINE)


def nl(t: TokenType):
    """Auto insert newline token"""
    return (t, TokenType.NEW_LINE)


class TestLexer(unittest.TestCase):
    def test_kv_tokens(self):
        text = 'username = "admin"'

        tokens = [t.type for t in Lexer(text).tokenize()]

        expected_tokens = [*KV_PAIR]

        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_section(self):
        text = """username = "admin"
                $network
                {
                    port = 8080
                }"""

        tokens = [t.type for t in Lexer(text).tokenize()]

        expected_tokens = [
            *KV_PAIR,
            *nl(TokenType.SECTION_NAME),
            *nl(TokenType.LBRACE),
            *KV_PAIR,
            *nl(TokenType.RBRACE),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_nested_section(self):
        text = """username = "admin"
                $network
                {
                    port = 8080
                    $local
                    {
                        port_num = 8300
                    }
                }"""

        tokens = [t.type for t in Lexer(text).tokenize()]

        expected_tokens = [
            *KV_PAIR,
            *nl(TokenType.SECTION_NAME),
            *nl(TokenType.LBRACE),
            *KV_PAIR,
            *nl(TokenType.SECTION_NAME),
            *nl(TokenType.LBRACE),
            *KV_PAIR,
            *nl(TokenType.RBRACE),
            *nl(TokenType.RBRACE),
        ]

        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()

import unittest
from lexer import Lexer
from tokens import Token, TokenType


class TestLexer(unittest.TestCase):
    def test_kv_tokens(self):
        text = 'username = "admin"'

        tokens = [t.type for t in Lexer(text).tokenize()]

        expected_tokens = [
            TokenType.KEY,
            TokenType.EQUALS,
            TokenType.VALUE,
            TokenType.NEWLINE,
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_tokenize_section(self):
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
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.SECTION_NAME, TokenType.NEWLINE),
            *(TokenType.RIGHT_PARN, TokenType.NEWLINE),
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.SECTION_NAME, TokenType.NEWLINE),
            *(TokenType.RIGHT_PARN, TokenType.NEWLINE),
            *(TokenType.KEY, TokenType.EQUALS, TokenType.VALUE, TokenType.NEWLINE),
            *(TokenType.LEFT_PARN, TokenType.NEWLINE),
            *(TokenType.LEFT_PARN, TokenType.NEWLINE),
        ]

        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()

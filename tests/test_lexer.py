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


if __name__ == "__main__":
    unittest.main()

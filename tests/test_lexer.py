import unittest
from lexer import Lexer
from tokens import Token, TokenType


class TestLexer(unittest.TestCase):
    def test_kv_tokens(self):
        text = 'username = "admin"'

        tokens = Lexer(text).tokenize()

        expected_tokens = [
            Token(type=TokenType.KEY, value="username", pos=(1, 9)),
            Token(type=TokenType.EQUALS, value=None, pos=(1, 9)),
            Token(type=TokenType.VALUE, value="admin", pos=(1, 14)),
            Token(type=TokenType.NEWLINE, value=None, pos=(1, 14)),
        ]

        self.assertEqual(
            tokens,
            expected_tokens,
        )


if __name__ == "__main__":
    unittest.main()

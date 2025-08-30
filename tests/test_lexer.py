import unittest
from lexer import Lexer
from tokens import Token, TokenType


class TestLexer(unittest.TestCase):
    def test_kv_tokens(self):
        text = 'username = "admin"'

        tokens = Lexer(text).tokenize()

        expected_tokens = [
            Token(type=TokenType.KEY, value="username", pos=(0, 0)),
            Token(type=TokenType.EQUALS, value=None, pos=(0, 0)),
            Token(type=TokenType.VALUE, value="admin", pos=(0, 0)),
            Token(type=TokenType.NEWLINE, value=None, pos=(0, 0)),
        ]

        self.assertEqual(tokens, expected_tokens)


if __name__ == "__main__":
    unittest.main()

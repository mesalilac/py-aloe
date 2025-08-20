from lexer import Lexer
from parser import Parser
from pprint import pprint


TEST_TEXT = """username = "admin"
password = "secret123"
timeout = 30
pi = 3.14159
max_retries = 5
enable_feature = "yes"
theme = "dark"
"""


def main():
    tokens = Lexer(TEST_TEXT).tokenize()

    pprint(tokens)

    config = Parser(tokens).parse()

    pprint(config)


if __name__ == "__main__":
    main()

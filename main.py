from lexer import Lexer
from parser import Parser

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
    config = Parser(tokens).parse()

    print(config)


if __name__ == "__main__":
    main()

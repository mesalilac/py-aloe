from lexer import Lexer
from parser import Parser


def main():
    text = """username = "admin"
password = "secret123"
timeout = 30
pi = 3.14159
max_retries = 5
enable_feature = "yes"
theme = "dark"
"""
    tokens = Lexer(text).tokenize()
    config = Parser(tokens).parse()

    print(config)


if __name__ == "__main__":
    main()

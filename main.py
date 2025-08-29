from lexer import Lexer
from parser import Parser, ParserSyntaxError
from pprint import pprint


TEST_TEXT = """username = "admin"
# Example comment.
password = "secret123"
timeout = 30
pi = 3.14159
max_retries = 5
enable_feature = "yes"
# UI theme, e.g [dark, light]
theme = "dark"
$network
{
    port = 8080
}
"""


def main():
    tokens = Lexer(TEST_TEXT).tokenize()

    pprint(tokens)

    try:
        config = Parser(tokens, TEST_TEXT).parse()

        pprint(config)
    except ParserSyntaxError as err:
        err.print()


if __name__ == "__main__":
    main()

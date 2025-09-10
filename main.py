from cfg import Cfg
from lexer import lex
from parser import parse, ParserSyntaxError
from pprint import pprint


TEST_TEXT = """username = "admin"
# Example comment.
password = "secret123"
timeout = 30
pi = 3.14159
max_retries = 5
enable_feature = true
# UI theme, e.g [dark, light]
theme = "dark"
@network
{
    port = 8080
    @local
    {
        port_num = 8300
    }
}
"""


def main():
    tokens = lex(TEST_TEXT)

    pprint(tokens)

    try:
        cfg = Cfg.from_text(TEST_TEXT)

        pprint(cfg.document.items)

        pprint(cfg.document.to_text())
    except ParserSyntaxError as err:
        err.print()


if __name__ == "__main__":
    main()

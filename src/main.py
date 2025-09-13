from py_cfg.cfg import Cfg
from py_cfg.lexer import lex
from py_cfg.parser import parse, ParserSyntaxError
from pprint import pprint


def main():
    text = """# global settings

app_name = "myapp"
version = "1.0.0"

@database {
    host = "localhost"
    port = 5432
    user = "admin"
    password = "secret"

    @pool {
        max_connections = 20
        timeout = 30
    }
}"""

    tokens = lex(text)

    pprint(tokens)

    # try:
    #     cfg = Cfg.from_file("example.cfg")

    #     pprint(cfg.document.items)

    #     pprint(cfg.document.to_text())
    # except ParserSyntaxError as err:
    #     err.print()


if __name__ == "__main__":
    main()

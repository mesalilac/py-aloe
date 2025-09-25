# from aloe.cfg import Cfg
from aloe.lexer import lex
from aloe.parser import parse, ParserSyntaxError
from pprint import pprint


def main():
    text = """# global settings

app_name = "myapp"
version = "1.0.0"
dependencies = [
    [1, 2, 3, [4, 5, 6]],
    "pk1",
    "pk2",
    # "pk3",
    "pk4",
    130,
    3.14
]

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

    try:
        document = parse("text", tokens=tokens, text=text)

        pprint(document._items)
    except ParserSyntaxError as err:
        err.print()

    # try:
    #     cfg = Cfg.from_file("example.cfg")

    #     pprint(cfg.document.items)

    #     pprint(cfg.document.to_text())
    # except ParserSyntaxError as err:
    #     err.print()


if __name__ == "__main__":
    main()

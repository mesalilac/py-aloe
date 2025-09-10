from py_cfg.cfg import Cfg
from py_cfg.lexer import lex
from py_cfg.parser import parse, ParserSyntaxError
from pprint import pprint


def main():
    try:
        cfg = Cfg.from_file("example.cfg")

        pprint(cfg.document.items)

        pprint(cfg.document.to_text())
    except ParserSyntaxError as err:
        err.print()


if __name__ == "__main__":
    main()

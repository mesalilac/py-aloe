from dataclasses import dataclass
from py_cfg.lexer import TokenType, Token
from py_cfg.ast import *
from py_cfg.symbols import SECTION_PREFIX


class ParserSyntaxError(Exception):
    def __init__(
        self,
        *,
        source: str,
        text: str,
        message: str,
        position: tuple[int, int],
    ):
        self.message: str = message
        self.position: tuple[int, int] = position
        self.source: str = source
        self.line: str = ""
        self.line_before: str | None = None
        self.line_after: str | None = None

        lines = text.splitlines()
        line_num, col_num = self.position
        line_index = line_num - 1
        if not (0 <= line_index < len(lines)):
            return
        if line_index > 0:
            self.line_before = lines[line_index - 1]
        self.line = lines[line_index]
        if line_index + 1 < len(lines):
            self.line_after = lines[line_index + 1]

    def __str__(self):
        line, column = self.position

        return f"{self.source}:{line}:{column}: {self.message}"

    def __repr__(self):
        return f"ParserSyntaxError(message: `{self.message}`, position: `{self.position}`,  source: `{self.source}`, line: `{self.line}`, line_before: `{self.line_before}`, line_after: `{self.line_after}`)"

    def print(self):
        line_num, col_num = self.position
        line_index = line_num - 1

        prefix_space = " " * len(str(line_num))
        empty_space = " " * max(col_num - 1, 0)

        def print_line(num: int, content: str | None = None):
            if content is not None:
                print(f" {num} | {content}")
            else:
                print(f" {prefix_space} |")

        print(f" {prefix_space} --> {self.source}:{line_num}:{col_num}")

        if self.line_before:
            print_line(line_index, self.line_before)

        print_line(line_num, self.line)

        print(f" {prefix_space} | {empty_space}^")
        print(f" {prefix_space} | {empty_space}| {self.message}")
        print_line(line_num)

        if self.line_after:
            print_line(line_index + 2, self.line_after)


@dataclass
class ParserState:
    index: int = 0


def parse(source: str, text: str, tokens: list[Token]) -> Document:
    items: list[AST_ItemType] = []

    state = ParserState()
    sections: list[SectionNode] = []

    def is_at_end() -> bool:
        return state.index >= len(tokens)

    def peek(offset: int = 0) -> Token | None:
        idx = state.index + offset

        if not tokens or is_at_end():
            return None

        return tokens[idx]

    def peek_behind(offset: int = 0) -> Token | None:
        idx = state.index - offset

        if not tokens or idx < 0 or is_at_end():
            return None

        return tokens[idx]

    def check(type_: TokenType, offset=0) -> bool:
        tok = peek(offset)

        return tok is not None and tok.type == type_

    def check_behind(type_: TokenType, offset=0) -> bool:
        tok = peek_behind(offset)

        return tok is not None and tok.type == type_

    def current() -> Token | None:
        return peek(0)

    def previous() -> Token | None:
        return peek_behind(1)

    def error(message: str, tok: Token | None = None) -> ParserSyntaxError:
        if tok is None:
            tok = current()

        position = tok.position if tok else (1, 1)

        return ParserSyntaxError(
            source=source, text=text, message=message, position=position
        )

    def advance(n=1) -> Token | None:
        if state.index < 0 or is_at_end():
            return None

        tok = tokens[state.index]

        state.index += n

        return tok

    def parse_array() -> Array:
        array = Array([])

        tok = current()

        if tok is None or tok.type != TokenType.LBRACKET:
            return array

        advance()

        tok = current()
        if tok is None:
            return array

        while not is_at_end() and tokens[state.index] != TokenType.RBRACKET:
            tok = current()
            if tok is None:
                return array

            match tok.type:
                case TokenType.COMMENT:
                    if tok.value is None:
                        return array

                    array.append_comment(str(tok.value))
                case TokenType.STRING | TokenType.NUMBER | TokenType.BOOLEAN:
                    if tok.value is None:
                        return array

                    array.append(tok.value)
                case TokenType.LBRACKET:
                    array.append(parse_array())
                case TokenType.RBRACKET:
                    break

            advance()

        return array

    while state.index < len(tokens) and tokens[state.index] != TokenType.EOF:
        token = current()
        assert token

        current_scope = items if len(sections) == 0 else sections[-1].body

        match token.type:
            case TokenType.ILLEGAL:
                error(f"Illegal character: {token.value}")
            case TokenType.NEWLINE:
                advance()
            case TokenType.COMMENT:
                current_scope.append(CommentNode(str(token.value)))
                advance()
            case TokenType.BLANK_LINE:
                current_scope.append(BlankLineNode())
                advance()
            case TokenType.EQUALS:
                prev_token = previous()
                next_token = peek(1)

                if (
                    prev_token is None
                    or prev_token.value is None
                    or prev_token.type != TokenType.IDENTIFIER
                ):
                    raise error("Expected an identifier before '='")
                if (
                    next_token is None
                    or next_token.value is None
                    or (
                        next_token.type != TokenType.STRING
                        and next_token.type != TokenType.NUMBER
                        and next_token.type != TokenType.BOOLEAN
                        and next_token.type != TokenType.LBRACKET
                    )
                ):
                    raise error("Expected a string/number/boolean/array[] after '='")

                if (
                    next_token.type == TokenType.STRING
                    or next_token.type == TokenType.NUMBER
                    or next_token.type == TokenType.BOOLEAN
                ):
                    current_scope.append(
                        AssignmentNode(
                            key=str(prev_token.value),
                            value=next_token.value,
                        )
                    )
                    advance(2)
                elif next_token.type == TokenType.LBRACKET:
                    # TODO: parse array
                    advance()
                    current_scope.append(
                        AssignmentNode(key=str(prev_token.value), value=parse_array())
                    )
                advance()
            case TokenType.SECTION_PREFIX:
                next_token = peek(1)
                brace_token = peek(2)
                is_inline = True

                if next_token is None or next_token.value is None:
                    raise error(
                        "Expected an identifier after section prefix", next_token
                    )

                if brace_token:
                    if brace_token.type == TokenType.LBRACE:
                        is_inline = True
                    else:
                        is_inline = False

                sections.append(
                    SectionNode(str(next_token.value), inline_lbrace=is_inline)
                )
                advance(2)
            case TokenType.LBRACE:
                if len(sections) == 0:
                    raise error("Unexpected '{' without section declaration")
                advance()
            case TokenType.RBRACE:
                if len(sections) == 0:
                    raise error("Unexpected '}' with no open section")
                section = sections.pop()

                if sections:
                    sections[-1].body.append(section)
                else:
                    items.append(section)

                advance()
            case _:
                advance()

    return Document(items)

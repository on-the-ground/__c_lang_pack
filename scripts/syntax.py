"""Syntax-only adapter for the pinned public lexical preprocessing contract."""
from antlr4 import Token
from antlr4.ListTokenSource import ListTokenSource
from antlr4.Token import CommonToken

CONTINUATION = {'=', '->', '-0>', '-1>', '-N>', ',', ':', '@', '$',
                '||', '&&', '==', '!=', '<=', '>=', '<', '>',
                '+', '-', '*', '/', '%', '!'}


def normalize(lexer, parser_class):
    # Keep lexer positions in the original source; whitespace/comments never
    # concatenate neighbors or contribute newlines inside a block comment.
    physical = []
    while True:
        token = lexer.nextToken()
        if token.channel == Token.DEFAULT_CHANNEL or token.type == Token.EOF:
            physical.append(token)
        if token.type == Token.EOF:
            break
    result, delimiters = [], []
    after_equals = head = window = False
    root_state = 0
    index = 0
    while index < len(physical):
        token = physical[index]
        index += 1
        previous = result[-1] if result else None
        if token.type == lexer.TERMINATOR:
            if delimiters or (previous and previous.text in CONTINUATION):
                continue
            if previous and previous.type == lexer.TERMINATOR:
                previous.stop = token.stop
                continue
            result.append(token)
            after_equals = window = False
            continue
        if token.type == Token.EOF:
            result.append(token)
            break
        statement_start = not delimiters and (previous is None or previous.type == lexer.TERMINATOR)
        if (statement_start and token.type == lexer.IDENTIFIER and token.text == 'root'
                and physical[index].type == lexer.IDENTIFIER):
            token.type = parser_class.ROOT
            root_state = 1
        elif root_state == 1:
            root_state = 2 if token.type == lexer.IDENTIFIER else 0
        elif root_state == 2:
            if token.type != lexer.HASH_QUALIFIER:
                root_state = 3 if token.text == '/' else 0
        elif root_state == 3:
            root_state = 0
            if token.type == lexer.NUMBER and '.' not in token.text:
                token.type = parser_class.ROOT_ARITY
        if window:
            window = False
            if token.text == '-' and index + 1 < len(physical):
                middle, end = physical[index:index + 2]
                if (middle.text in ('0', '1', 'N') and end.text == '>'
                        and token.stop + 1 == middle.start and middle.stop + 1 == end.start):
                    merged = CommonToken(token.source, parser_class.MULTIPLICITY_ARROW,
                                         Token.DEFAULT_CHANNEL, token.start, end.stop)
                    merged.text = '-' + middle.text + '>'
                    merged.line, merged.column = token.line, token.column
                    token = merged
                    index += 2
        if after_equals:
            after_equals = False
            head = token.text == '['
        if token.text == '=' and not delimiters:
            after_equals = True
        if token.text in ('[', '(', '{'):
            delimiters.append(token.text)
        elif token.text in (']', ')', '}') and delimiters:
            delimiters.pop()  # The parser diagnoses mismatched closing kinds.
            if not delimiters and head:
                head, window = False, True
        result.append(token)
    return ListTokenSource(result)

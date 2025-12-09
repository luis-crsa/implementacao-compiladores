from collections import deque

class ParseError(Exception):
    pass

def map_token_to_terminal(token):
    return token.type

def parse(token_iter, table, start_symbol, terminals, nonterminals):
    stack = deque()
    stack.append('EOF')
    stack.append(start_symbol)

    tokens = iter(token_iter)
    look = next(tokens)
    look_term = map_token_to_terminal(look)

    while stack:
        top = stack.pop()
        if top == 'EOF' and look_term == 'EOF':
            return True
        if top in terminals:
            if top == look_term:
                try:
                    look = next(tokens)
                    look_term = map_token_to_terminal(look)
                except StopIteration:
                    raise ParseError("Unexpected end of tokens")
            else:
                raise ParseError(f"Syntax error at line {look.line}, col {look.col}: unexpected token {look_term} ('{look.value}'), expected terminal {top}")
        elif top in nonterminals:
            entry = table.get(top, {}).get(look_term)
            if entry is None:
                expected = sorted(table.get(top, {}).keys())
                raise ParseError(f"Syntax error at line {look.line}, col {look.col}: no rule for nonterminal {top} with lookahead {look_term} ('{look.value}'). Expected one of: {expected}")
            if entry == []:
                continue
            for sym in reversed(entry):
                stack.append(sym)
        else:
            raise ParseError(f"Internal parser error: unknown symbol on stack: {top}")
    return False
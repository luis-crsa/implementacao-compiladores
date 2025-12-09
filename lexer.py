import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'col'])

class LexerError(Exception):
    pass

token_specification = [
    ('LINE_COMMENT', r'//[^\n]*'),
    ('BLOCK_COMMENT', r'/\*[\s\S]*?\*/'),
    ('WHITESPACE', r'[ \t\r\n]+'),

    ('NUM_REAL', r'\d+\.\d+([eE][+-]?\d+)?'),
    ('NUM_INT',  r'\d+'),
    ('CADEIA',   r'"([^"\\\n]|\\.)*"'),

    ('POT',       r'\*\*'),
    ('INCR',      r'\+\+'),
    ('DECR',      r'--'),

    ('IGUALDADE', r'=='),
    ('DIFERENTE', r'!='),
    ('MENORIGUAL',r'<='),
    ('MAIORIGUAL',r'>='),

    ('E_LOGICO',  r'&&'),
    ('OU_LOGICO', r'\|\|'),

    ('MAIN',    r'\bmain\b'),
    ('SE',      r'\bif\b'),
    ('SENAO',   r'\belse\b'),
    ('WHILE',   r'\bwhile\b'),
    ('DO',      r'\bdo\b'),
    ('FOR',     r'\bfor\b'),
    ('FUNCAO',  r'\bfunction\b'),
    ('RETORNO', r'\breturn\b'),

    ('INTEIRO',  r'\bint\b'),
    ('REAL',     r'\bfloat\b'),
    ('BOOLEANO', r'\bboolean\b'),
    ('TEXTO',    r'\bstring\b'),
    ('VERDADEIRO', r'\btrue\b'),
    ('FALSO',      r'\bfalse\b'),

    ('ID',      r'[A-Za-z_][A-Za-z0-9_]*'),

    ('MAIS',    r'\+'),
    ('MENOS',   r'-'),
    ('MULT',    r'\*'),
    ('DIV',     r'/'),
    ('MOD',     r'%'),
    ('NAO',     r'!'),
    ('IGUAL',   r'='),
    ('MENOR',   r'<'),
    ('MAIOR',   r'>'),

    ('PONTOEVIRG', r';'),
    ('VIRGULA',    r','),
    ('LPAREN',     r'\('),
    ('RPAREN',     r'\)'),
    ('LBRACE',     r'\{'),
    ('RBRACE',     r'\}'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

def tokenize(code):
    pos = 0
    line = 1
    col = 1
    end = len(code)
    m = get_token(code, pos)
    while m:
        typ = m.lastgroup
        val = m.group(typ)
        if typ == 'WHITESPACE' or typ in ('LINE_COMMENT','BLOCK_COMMENT'):
            pass
        else:
            last_nl = code.rfind('\n', 0, m.start())
            if last_nl < 0:
                col = m.start() + 1
            else:
                col = m.start() - last_nl
            yield Token(typ, val, line, col)
        nl_count = val.count('\n')
        if nl_count:
            line += nl_count
        pos = m.end()
        m = get_token(code, pos)
    if pos != end:
        snippet = code[pos:pos+20]
        raise LexerError(f'Unexpected character {code[pos]!r} at index {pos}: ...{snippet}...')
    yield Token('EOF', '', line, col)

# run_parser.py
import os
from grammar.grammar_ll1 import GRAMMAR
from parser.firts_follow import compute_first, compute_follow
from parser.table_builder import build_ll1_table
from parser.ll1_parser import parse
from lexer import tokenize

def prepare_grammar():
    prods = {}
    for A, plist in GRAMMAR['productions'].items():
        prods[A] = []
        for p in plist:
            # normalize epsilon: represent epsilon as empty list []
            if p == [] or p == ['ε'] or p == 'ε':
                prods[A].append([])
            else:
                prods[A].append(list(p))
    terminals = set(GRAMMAR['terminals'])
    nonterminals = set(GRAMMAR['nonterminals'])
    return prods, terminals, nonterminals, GRAMMAR['start_symbol']

def main():
    prods, terminals, nonterminals, start = prepare_grammar()
    print("Computing FIRST sets...")
    first = compute_first(prods, terminals, nonterminals)
    print("Computing FOLLOW sets...")
    follow = compute_follow(prods, start, terminals, nonterminals, first)

    print("\n--- SELECTED FIRST sets ---")
    for k in ["Program","DeclList","Decl","FuncDecl","VarDecl","MainDecl","Type"]:
        print(f"{k}: {sorted(first.get(k, []))}")
    print("\n--- SELECTED FOLLOW sets ---")
    for k in ["Program","DeclList","Decl","FuncDecl","VarDecl","MainDecl","Type"]:
        print(f"{k}: {sorted(follow.get(k, []))}")

    print("\nBuilding LL(1) table...")
    table = build_ll1_table(prods, terminals, nonterminals, first, follow)
    print("Table built successfully (no conflicts).")

    example_path = os.path.join('examples','ex1.minilang')
    if os.path.exists(example_path):
        with open(example_path, 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        code = """
function f() {
    int a;
    a = 1;
    if (a < 2) {
        a = a + 1;
    } else {
        a = a - 1;
    }
}

main {
    int a;
    a = 5;
    a++;
    a = a + 2;
}
"""

    print("\nTokenizing input...")
    tokens = list(tokenize(code))
    print("Tokens:", [(t.type, t.value) for t in tokens[:120]])

    print("\nParsing...")
    try:
        ok = parse(iter(tokens), table, start, terminals, nonterminals)
        if ok:
            print("Input accepted by grammar (parser returned True).")
        else:
            print("Input not accepted (parser returned False).")
    except Exception as e:
        print("Parsing error:", e)

if __name__ == '__main__':
    main()

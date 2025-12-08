# parser/table_builder.py
from parser.firts_follow import EPS, first_of_sequence

def build_ll1_table(productions, terminals, nonterminals, first, follow):
    table = {A:{} for A in nonterminals}
    conflicts = []
    for A in nonterminals:
        for prod in productions.get(A, []):
            prod_first = first_of_sequence(prod, first)
            for a in (prod_first - {EPS}):
                if a in table[A]:
                    conflicts.append((A,a,table[A][a],prod))
                else:
                    table[A][a] = prod
            if EPS in prod_first:
                for b in follow[A]:
                    if b in table[A]:
                        conflicts.append((A,b,table[A][b],prod))
                    else:
                        table[A][b] = prod
    if conflicts:
        msg = ["LL(1) conflicts detected:"]
        for (A,a,exist,conf) in conflicts:
            msg.append(f" Conflict at M[{A},{a}]: existing {exist} vs new {conf}")
        raise Exception("\n".join(msg))
    return table

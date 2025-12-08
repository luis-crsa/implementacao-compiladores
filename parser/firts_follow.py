# parser/firts_follow.py
EPS = 'EPS'

def compute_first(productions, terminals, nonterminals):
    # initialize
    first = {A:set() for A in nonterminals}
    for t in terminals:
        first[t] = {t}

    changed = True
    while changed:
        changed = False
        for A in nonterminals:
            for rhs in productions.get(A, []):
                # epsilon production
                if rhs == []:
                    if EPS not in first[A]:
                        first[A].add(EPS); changed = True
                    continue
                seq_first = first_of_sequence(rhs, first)
                before = len(first[A])
                first[A].update(seq_first)
                if len(first[A]) != before:
                    changed = True
    return first

def first_of_sequence(seq, first):
    result = set()
    for symbol in seq:
        if symbol == 'ε':
            result.add(EPS)
            continue
        # symbol must be in first
        if symbol not in first:
            # unknown symbol — skip to avoid crash (defensive)
            continue
        for x in first[symbol]:
            if x != EPS:
                result.add(x)
        if EPS not in first[symbol]:
            break
    else:
        result.add(EPS)
    return result

def compute_follow(productions, start_symbol, terminals, nonterminals, first):
    follow = {A:set() for A in nonterminals}
    follow[start_symbol].add('EOF')
    changed = True
    while changed:
        changed = False
        for A in nonterminals:
            for rhs in productions.get(A, []):
                for i, B in enumerate(rhs):
                    if B not in nonterminals:
                        continue
                    beta = rhs[i+1:]
                    if beta:
                        first_beta = first_of_sequence(beta, first)
                        without_eps = {x for x in first_beta if x != EPS}
                        before = len(follow[B])
                        follow[B].update(without_eps)
                        if len(follow[B]) != before:
                            changed = True
                        if EPS in first_beta:
                            before = len(follow[B])
                            follow[B].update(follow[A])
                            if len(follow[B]) != before:
                                changed = True
                    else:
                        before = len(follow[B])
                        follow[B].update(follow[A])
                        if len(follow[B]) != before:
                            changed = True
    return follow

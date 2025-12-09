EPS = 'ε'

def compute_first(productions, terminals, nonterminals):
    # Inicializa os conjuntos FIRST
    first = {A:set() for A in nonterminals}
    for t in terminals:
        first[t] = {t}

    changed = True
    while changed:
        changed = False
        for A in nonterminals:
            for rhs in productions.get(A, []):
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
        
        if symbol not in first:
            # Símbolo desconhecido, ignora
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
    # Inicializa os conjuntos FOLLOW
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
                        
                        # Regra 1: FOLLOW(B) = FOLLOW(B) U (FIRST(beta) - {EPS})
                        before = len(follow[B])
                        follow[B].update(without_eps)
                        if len(follow[B]) != before:
                            changed = True
                        
                        # Regra 2: Se EPS in FIRST(beta), FOLLOW(B) = FOLLOW(B) U FOLLOW(A)
                        if EPS in first_beta:
                            before = len(follow[B])
                            follow[B].update(follow[A])
                            if len(follow[B]) != before:
                                changed = True
                    else:
                        # Regra 3: Se beta é vazio, FOLLOW(B) = FOLLOW(B) U FOLLOW(A)
                        before = len(follow[B])
                        follow[B].update(follow[A])
                        if len(follow[B]) != before:
                            changed = True
    return follow
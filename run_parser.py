import os
import csv
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
            # Normaliza o épsilon (produção vazia) como lista vazia
            if p == [] or p == ['ε'] or p == 'ε':
                prods[A].append([])
            else:
                prods[A].append(list(p))
    terminals = set(GRAMMAR['terminals'])
    nonterminals = set(GRAMMAR['nonterminals'])
    return prods, terminals, nonterminals, GRAMMAR['start_symbol']


def create_results_folder(folder_name="resultados"):
    """Cria a pasta de resultados se ela não existir."""
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


def export_first_follow_to_csv(first, follow, nonterminals, folder_name):
    """Exporta os conjuntos FIRST e FOLLOW para um arquivo CSV."""
    filename = os.path.join(folder_name, "first_follow_sets.csv")
    ordered_nonterminals = sorted(list(nonterminals))
    
    header = ["Nao-Terminal", "Conjunto FIRST", "Conjunto FOLLOW"]
    data = []
    
    for nt in ordered_nonterminals:
        first_set_str = ", ".join(sorted([s if s != 'ε' else 'EPSILON' for s in first.get(nt, [])]))
        follow_set_str = ", ".join(sorted(follow.get(nt, [])))
        
        data.append([nt, first_set_str, follow_set_str])

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data)
        print(f"[✅] Conjuntos FIRST/FOLLOW exportados para: {filename}")
    except Exception as e:
        print(f"[❌] Erro ao exportar FIRST/FOLLOW CSV: {e}")


def export_ll1_table_to_csv(table, nonterminals, terminals, folder_name):
    """Exporta a tabela LL(1) para um arquivo CSV."""
    filename = os.path.join(folder_name, "tabela_ll1.csv")
    
    ordered_nonterminals = sorted(list(nonterminals))
    header_terminals = sorted([t for t in terminals if t not in ('ε', 'EPS')])
    
    header = ["Nao-Terminal"] + header_terminals
    data = []
    
    for nt in ordered_nonterminals:
        row = [nt]
        for term in header_terminals:
            entry = table.get(nt, {}).get(term)
            
            if entry is not None:
                # Formato da produção: NT -> T1 T2... ou NT -> [] (para épsilon)
                prod_str = f"{nt} -> {' '.join(entry)}" if entry else f"{nt} -> []"
            else:
                prod_str = ""
            
            row.append(prod_str)
        data.append(row)

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data)
        print(f"[✅] Tabela LL(1) exportada para: {filename}")
    except Exception as e:
        print(f"[❌] Erro ao exportar LL(1) CSV: {e}")


def export_tokens_to_txt(tokens, folder_name):
    """Exporta a cadeia de tokens para um arquivo TXT."""
    filename = os.path.join(folder_name, "cadeia_de_tokens.txt")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("--- CADEIA DE TOKENS ---\n")
            
            for token in tokens:
                f.write(f"({token.type}, '{token.value}') Linha: {token.line}, Coluna: {token.col}\n")
            
            f.write("\n--- FIM DA CADEIA ---\n")

        print(f"[✅] Cadeia de Tokens exportada para: {filename}")
    except Exception as e:
        print(f"[❌] Erro ao exportar TXT de Tokens: {e}")


def main():
    RESULTS_FOLDER = create_results_folder()

    prods, terminals, nonterminals, start = prepare_grammar()
    ordered_nonterminals = sorted(list(nonterminals)) 
    
    print("Calculando conjuntos FIRST...")
    first = compute_first(prods, terminals, nonterminals)
    print("Calculando conjuntos FOLLOW...")
    follow = compute_follow(prods, start, terminals, nonterminals, first)

    # Geração da Tabela LL(1)
    print("\nConstruindo Tabela LL(1)...")
    try:
        table = build_ll1_table(prods, terminals, nonterminals, first, follow)
        print("Tabela construída com sucesso (sem conflitos).")
    except Exception as e:
        print("Erro na Tabela LL(1):", e)
        return

    # Exportações para CSV/TXT
    export_first_follow_to_csv(first, follow, nonterminals, RESULTS_FOLDER)
    export_ll1_table_to_csv(table, nonterminals, terminals, RESULTS_FOLDER)

    # --- Impressão dos Conjuntos (Console) ---
    print("\n## 📋 TODOS OS CONJUNTOS FIRST ##")
    for k in ordered_nonterminals:
        first_set_str = sorted([s if s != 'ε' else 'EPSILON' for s in first.get(k, [])])
        print(f"{k}: {first_set_str}")

    print("\n## 🧭 TODOS OS CONJUNTOS FOLLOW ##")
    for k in ordered_nonterminals:
        print(f"{k}: {sorted(follow.get(k, []))}")
        
    # --- Impressão da Tabela LL(1) (Console/Markdown) ---
    print("\n## 📊 TABELA DE PARSING LL(1) ##")
    
    header_terminals = sorted([t for t in terminals if t not in ('ε', 'EPS')])
    
    header = "| Não-Terminal | " + " | ".join(header_terminals) + " |"
    separator = "| --- |" + " --- |" * len(header_terminals)

    print(header)
    print(separator)

    for nt in ordered_nonterminals:
        row = f"| **{nt}** |"
        for term in header_terminals:
            entry = table.get(nt, {}).get(term)
            
            if entry is not None:
                prod_str = " -> " + " ".join(entry) if entry else " -> []"
            else:
                prod_str = ""
            
            row += f" {prod_str[:15]} |" 
        print(row)
    
    print("\n" + "="*50 + "\n")
    
    # --- Execução e Tokenização ---
    example_path = os.path.join('examples','ex.ms')
    if os.path.exists(example_path):
        with open(example_path, 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        # Código de exemplo padrão
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

    print("\nTokenizando a entrada...")
    tokens = list(tokenize(code))
    print("Tokens (Primeiros 120):", [(t.type, t.value) for t in tokens[:120]])

    # Exportação da Cadeia de Tokens
    export_tokens_to_txt(tokens, RESULTS_FOLDER)

    # --- Parsing ---
    print("\nAnalisando...")
    try:
        ok = parse(iter(tokens), table, start, terminals, nonterminals)
        if ok:
            print("Entrada aceita pela gramática (parser retornou True).")
        else:
            print("Entrada não aceita (parser retornou False).")
    except Exception as e:
        print("Erro de análise (Parsing):", e)

if __name__ == '__main__':
    main()
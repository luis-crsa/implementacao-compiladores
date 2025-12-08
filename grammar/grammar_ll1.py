GRAMMAR = {
    "start_symbol": "Program",

    "nonterminals": [
        "Program","DeclList","DeclList_","Decl",
        "FuncDecl","ParamList","ParamList_","Param",
        "VarDecl","MainDecl","Type",
        "Block","StmtList","StmtList_",
        "Stmt","MatchedStmt","UnmatchedStmt",
        "SimpleStmt","SimpleStmtTail",
        "ForInitExpr","ForUpdateExpr",
        "Chamada","ArgList","ArgList_",
        "Expr","ExprOr","ExprOr_","ExprAnd","ExprAnd_",
        "ExprEq","ExprEq_","ExprRel","ExprRel_",
        "ExprAdd","ExprAdd_","ExprMul","ExprMul_",
        "ExprUnary","Primary","PrimaryTail"
    ],

    "terminals": [
        "FUNCAO","MAIN","SE","SENAO",
        "WHILE","DO","FOR","RETORNO",
        "INTEIRO","REAL","BOOLEANO","TEXTO",
        "ID","NUM_INT","NUM_REAL","CADEIA",
        "VERDADEIRO","FALSO",
        "INCR","DECR",
        "IGUAL","IGUALDADE","DIFERENTE",
        "MENOR","MENORIGUAL","MAIOR","MAIORIGUAL",
        "MAIS","MENOS","MULT","DIV","MOD",
        "E_LOGICO","OU_LOGICO","NAO",
        "LPAREN","RPAREN","LBRACE","RBRACE",
        "PONTOEVIRG","VIRGULA",
        "EOF"
    ],

    "productions": {

        # Program
        "Program": [["DeclList"]],

        # Declarations
        "DeclList": [["Decl","DeclList_"]],
        "DeclList_": [["Decl","DeclList_"], ["ε"]],
        "Decl": [["FuncDecl"], ["VarDecl"], ["MainDecl"]],

        # Functions
        "FuncDecl": [["FUNCAO","ID","LPAREN","ParamList","RPAREN","Block"]],
        "ParamList": [["Param","ParamList_"], ["ε"]],
        "ParamList_": [["VIRGULA","Param","ParamList_"], ["ε"]],
        "Param": [["Type","ID"]],

        # Variables and main
        "VarDecl": [["Type","ID","PONTOEVIRG"]],
        "MainDecl": [["MAIN","Block"]],
        "Type": [["INTEIRO"], ["REAL"], ["BOOLEANO"], ["TEXTO"]],

        # Block
        "Block": [["LBRACE","StmtList","RBRACE"]],
        "StmtList": [["Stmt","StmtList_"], ["ε"]],
        "StmtList_": [["Stmt","StmtList_"], ["ε"]],

        # Statements
        "Stmt": [["MatchedStmt"], ["UnmatchedStmt"]],

        # MatchedStmt = if com else + demais statements
        "MatchedStmt": [
            ["SE","LPAREN","Expr","RPAREN","MatchedStmt","SENAO","MatchedStmt"],
            ["WHILE","LPAREN","Expr","RPAREN","MatchedStmt"],
            ["DO","Stmt","WHILE","LPAREN","Expr","RPAREN","PONTOEVIRG"],
            ["FOR","LPAREN","ForInitExpr","PONTOEVIRG","Expr","PONTOEVIRG","ForUpdateExpr","RPAREN","MatchedStmt"],
            ["Block"],
            ["SimpleStmt","PONTOEVIRG"],
            ["RETORNO","Expr","PONTOEVIRG"],
            ["VarDecl"]
        ],

        # UnmatchedStmt = if sem else ou dangling else
        "UnmatchedStmt": [
            ["SE","LPAREN","Expr","RPAREN","Stmt"],
            ["SE","LPAREN","Expr","RPAREN","MatchedStmt","SENAO","UnmatchedStmt"]
        ],

        # Simple statements
        "SimpleStmt": [["ID","SimpleStmtTail"]],
        "SimpleStmtTail": [
            ["IGUAL","Expr"],
            ["INCR"],
            ["DECR"],
            ["LPAREN","ArgList","RPAREN"]
        ],

        # For expressions
        "ForInitExpr": [["SimpleStmt"], ["ε"]],
        "ForUpdateExpr": [["SimpleStmt"], ["ε"]],

        # Function calls
        "Chamada": [["ID","LPAREN","ArgList","RPAREN"]],
        "ArgList": [["Expr","ArgList_"], ["ε"]],
        "ArgList_": [["VIRGULA","Expr","ArgList_"], ["ε"]],

        # Expressions
        "Expr": [["ExprOr"]],
        "ExprOr": [["ExprAnd","ExprOr_"]],
        "ExprOr_": [["OU_LOGICO","ExprAnd","ExprOr_"], ["ε"]],
        "ExprAnd": [["ExprEq","ExprAnd_"]],
        "ExprAnd_": [["E_LOGICO","ExprEq","ExprAnd_"], ["ε"]],
        "ExprEq": [["ExprRel","ExprEq_"]],
        "ExprEq_": [
            ["IGUALDADE","ExprRel","ExprEq_"],
            ["DIFERENTE","ExprRel","ExprEq_"],
            ["ε"]
        ],
        "ExprRel": [["ExprAdd","ExprRel_"]],
        "ExprRel_": [
            ["MENOR","ExprAdd","ExprRel_"],
            ["MENORIGUAL","ExprAdd","ExprRel_"],
            ["MAIOR","ExprAdd","ExprRel_"],
            ["MAIORIGUAL","ExprAdd","ExprRel_"],
            ["ε"]
        ],
        "ExprAdd": [["ExprMul","ExprAdd_"]],
        "ExprAdd_": [
            ["MAIS","ExprMul","ExprAdd_"],
            ["MENOS","ExprMul","ExprAdd_"],
            ["ε"]
        ],
        "ExprMul": [["ExprUnary","ExprMul_"]],
        "ExprMul_": [
            ["MULT","ExprUnary","ExprMul_"],
            ["DIV","ExprUnary","ExprMul_"],
            ["MOD","ExprUnary","ExprMul_"],
            ["ε"]
        ],
        "ExprUnary": [
            ["MENOS","ExprUnary"],
            ["NAO","ExprUnary"],
            ["Primary"]
        ],
        "Primary": [
            ["ID","PrimaryTail"],
            ["NUM_INT"],
            ["NUM_REAL"],
            ["CADEIA"],
            ["VERDADEIRO"],
            ["FALSO"],
            ["LPAREN","Expr","RPAREN"]
        ],
        "PrimaryTail": [
            ["LPAREN","ArgList","RPAREN"],
            ["INCR"],
            ["DECR"],
            ["ε"]
        ]
    }
}

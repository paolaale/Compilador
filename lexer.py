import ply.lex as lex

# Reserved word
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'int' : 'INT',
    'bool' : 'BOOL',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'string' : 'STRING',
    'void' : 'VOID',
    'program' : 'PROGRAM',
    'while' : 'WHILE',
    'do': 'DO',
    'from' : 'FROM',
    'until' : 'UNTIL',
    'inherits' : 'INHERITS',
    'write' : 'WRITE',
    'read' : 'READ',
    'class' : 'CLASS',
    'return' : 'RETURN',
    'and' : 'AND',
    'or' : 'OR',
    'main' : 'MAIN',
    'func' : 'FUNC',
    'var' : 'VAR'
}

# Tokens
tokens = [
    'CTEI', 'CTEF', 'CTESTRING', 'CTECHAR', 'ID',
    'RELOP', 'PLUS', 'MINUS', 'DIVIDE', 'TIMES',
    'EQUAL', 'TWOPOINTS', 'SEMICOLON', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE', 'POINT'
] + list(reserved.values())

# Regular expression rules
t_CTEI = r'[+-]?[0-9]+'
t_CTEF = r'[+-]?([0-9]+)(\.)([0-9]+)?'
t_CTESTRING = r'\".*?\"' 
t_CTECHAR = r'\'.?\'' 
t_RELOP = r'(<)|(>)|(>=)|(<=)|(==)|(!=)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'/'
t_TIMES = r'\*'
t_EQUAL = r'='
t_TWOPOINTS = r'\:'
t_POINT = r'\.'
t_SEMICOLON = r'\;'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

# Ignore Characters
t_ignore =' \t\n'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value,'ID') # Check for reserved words
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex()

""" # Test 
data = ''' > + 4.5 * "abc" 3 , . : ; 'a' int = -20 -709.89 ({)} A00821971 if do then # array[] inherits class $ . and or alan'''
 
# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break # No more input
    print(tok)  """
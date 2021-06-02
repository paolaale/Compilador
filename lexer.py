# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 02/06/2021

import ply.lex as lex

# Reserved word
reserved = {
    'if' : 'IF',
    'then' : 'THEN',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'int' : 'INT',
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'void' : 'VOID',
    'program' : 'PROGRAM',
    'while' : 'WHILE',
    'do': 'DO',
    'end' : 'END',
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
    'init' : 'INIT',
    'funct' : 'FUNCT',
    'var' : 'VAR',
    'call' : 'CALL',
}

# Tokens
tokens = [
    'CTEI', 'CTEF', 'CTESTRING', 'CTECHAR', 'ID', 'OBJECT',
    'RELOP', 'PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'EQUAL', 
    'TWOPOINTS', 'SEMICOLON', 'COMMA', 'LPAREN', 'RPAREN', 
    'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'POINT'
] + list(reserved.values())

# Regular expression rules
t_CTEI = r'[+-]?[0-9]+'
t_CTEF = r'[+-]?([0-9]+)(\.)([0-9]+)?'
t_CTESTRING = r'\".*?\"' 
t_CTECHAR = r'\'.?\'' 
t_RELOP = r'(>=)|(<=)|(<)|(>)|(==)|(!=)'
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

def t_OBJECT(t):
    r'[A-Z_][a-z_0-9_]*'
    t.type = reserved.get(t.value,'OBJECT') # Check for reserved words
    return t

def t_ID(t):
    r'[a-z_][a-zA-Z_0-9_]*'
    t.type = reserved.get(t.value,'ID') # Check for reserved words
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build lexer
lexer = lex.lex()

import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    'program : PROGRAM ID TWOPOINTS program_aux main'

def p_program_aux(p):
    '''program_aux : dec_vars classes functions
                | classes functions
                | functions
                | empty
    '''
def p_dec_vars(p):
    'vars: type_vars dec_vars_aux SEMICOLON'

def p_type_vars(p):
    '''type_vars : type_aux
            | type_aux LBRACKET exp RBRACKET
            | type_aux LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''

def p_dec_vars_aux(p):
    '''dec_vars_aux : ID
                | ID COMMA dec_vars_aux'''

def p_functions(p):
    'functions: functType ID LPAREN params RPAREN LBRACE functBody return RBRACE'

def p_functType(p):
    '''functType : VOID 
                | type'''


def p_params(p):
    '''params : type ID
                | type ID COMMA params
                | empty'''

def p_type(p):
    '''type : type_aux
            | type_aux LBRACKET RBRACKET
            | type_aux LBRACKET RBRACKET LBRACKET RBRACKET'''

def p_type_aux(p):
    '''type_aux : INT
            | FLOAT
            | CHAR
            | STRING
            | BOOL
            | ID'''
    p[0] = 'type_aux'

def p_functBody(p):
    '''functBody : statutes
                | dec_vars statutes'''

def p_return(p): 
    '''return : RETURN expression
                | empty'''

def p_statutes(p):
    '''statutes : assignation 
                | call
                | read
                | write
                | condition
                | while
                | for'''

def p_assignation(p):
    'assignation : vars EQUAL expression'

def p_vars(p):
    '''vars : ID 
            | ID vars_aux'''

def p_vars_aux(p): 
    '''vars_aux : LBRACKET exp RBRACKET 
                | LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''

def p_expression(p):
    '''expression : expression_aux 
                    | expression_aux RELOP expression_aux'''

def p_expressionType(p):
    '''expressionType : exp
                        | call'''


def p_empty(p):
    'empty :  '
    print("This function is called")
    p[0] = "empty" 

def p_error(p):
    print("Syntax error en: ", p.type) 

if __name__ == '__main__':

    parser = yacc.yacc()

    file = input()
    fileData = open(file,'r')

    text = ""

    for line in fileData:
        try:
             text = text + line.strip()
        except EOFError:
            break
        
    if text:
            #isAccepted = parser.parse(lexer.tokenize(text))
            isAccepted = parser.parse(text)

            if isAccepted != None:
                print("Programa aceptado ")
            else:
                print("Error en el programa");
import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    'program : PROGRAM ID TWOPOINTS program_aux main'

def p_program_aux(p):
    'program_aux : dec_vars class_aux functions_aux'

def p_class_aux(p):
    '''class_aux : class 
                | class class_aux
                | empty'''

def p_functions_aux(p):
    '''functions_aux : functions 
                | empty'''

def p_dec_vars(p):
    '''vars : type_vars dec_vars_aux SEMICOLON 
            | type_vars dec_vars_aux SEMICOLON dec_vars
            | empty'''

def p_type_vars(p):
    '''type_vars : type_aux
            | type_aux LBRACKET exp RBRACKET
            | type_aux LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''

def p_dec_vars_aux(p):
    '''dec_vars_aux : ID
                    | ID COMMA dec_vars_aux'''

def p_functions(p):
    '''functions : functType ID LPAREN RPAREN LBRACE functBody return RBRACE 
                 | functType ID LPAREN params RPAREN LBRACE functBody return RBRACE
                 | functType ID LPAREN RPAREN LBRACE functBody return RBRACE functions
                 | functType ID LPAREN params RPAREN LBRACE functBody return RBRACE functions'''

def p_functType(p):
    '''functType : VOID 
                | type'''

def p_params(p):
    '''params : type ID
                | type ID COMMA params'''

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
                | call SEMICOLON
                | read
                | write
                | condition
                | while
                | for'''

def p_assignation(p):
    'assignation : vars EQUAL expression SEMICOLON'

def p_write(p):
    'write : WRITE LPAREN write_aux RPAREN SEMICOLON'

def p_write_aux(p):
    '''write_aux : expression
                | expression COMMA write_aux'''

def p_condition(p):
    'condition : IF condition_aux'

def p_condition_aux(p):
    '''condition_aux : LPAREN expression RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_2
                    | LPAREN expression RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_2 ELSE LBRACE statutes_aux RBRACE'''

def p_statutes_aux(p):
    '''statutes_aux : statutes 
                    | statutes statutes_aux'''

def p_condition_aux_2(p): 
    '''condition_aux_2 : ELIF condition_aux
                        | empty'''

def p_while(p):
    'while : WHILE LPAREN expression RPAREN DO LBRACE statutes_aux RBRACE'

def p_for(p):
    'for : FROM assignation UNTIL expression DO LBRACE statutes_aux RBRACE'

def p_class(p):
    '''class : CLASS ID LBRRACE dec_vars functions RRBRACE
               | CLASS ID INHERITTS ID LBRACE dec_vars functions RBRACE'''

def p_main(p):
    '''main : MAIN LBRACE statutes_aux RBRACE
            | MAIN LBRACE dec_vars statutes_aux RBRACE'''

def p_expression(p):
    '''expression : expression_aux 
                    | expression_aux RELOP expression_aux
                    | expression_aux AND expression_aux
                    | expression_aux OR expression_aux'''

def p_expression_aux(p):
    '''expression_aux : call
                        | exp'''

def p_call(p):
    '''call : ID LPAREN call_aux RPAREN
            | ID POINT ID LPAREN call_aux RPAREN'''

def p_call_aux(p):
    '''call_aux : call_aux_2 
                | empty'''

def p_call_aux2(p):
    '''call_aux_2 : exp 
                | exp COMMA call_aux2'''

def p_read(p):
    '''read : READ LPAREN read_aux RPAREN SEMICOLON'''

def p_read_aux(p):
    '''read_aux : vars
                | vars COMMA read_aux'''

def p_vars(p):
    '''vars : ID 
            | ID vars_aux'''

def p_vars_aux(p): 
    '''vars_aux : LBRACKET exp RBRACKET 
                | LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''

def p_exp(p):
    '''exp : term 
            | term PLUS exp
            | term MINUS exp'''

def p_term(p):
    '''term : factor
                | factor TIMES term
                | factor DIVIDE term'''

def p_factor(p):
    '''factor :  PLUS cte 
            | MINUS cte 
            | cte 
            | LP expresion RP'''

def p_cte(p):
    '''cte : ID
            | CTEI
            | CTEF
            | CTESTRING
            | CTECHAR'''

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
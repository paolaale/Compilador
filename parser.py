import ply.yacc as yacc
from lexer import tokens # Get the token list from the lexer

def p_program(p):
    'program : PROGRAM ID TWOPOINTS program_aux main'
    p.type = 'program'

def p_program_aux(p):
    'program_aux : dec_vars class_aux functions_aux'
    p.type = 'program'

def p_class_aux(p):
    '''class_aux : class 
                | class class_aux
                | empty'''
    p.type = 'class'

def p_functions_aux(p):
    '''functions_aux : functions 
                     | empty'''
    p.type = 'function'

def p_dec_vars(p):
    '''dec_vars : type_vars dec_vars_aux SEMICOLON 
                | type_vars dec_vars_aux SEMICOLON dec_vars
                | empty'''
    p.type = 'dec_var'

def p_type_vars(p):
    '''type_vars : type_aux
                | type_aux LBRACKET exp RBRACKET
                | type_aux LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''
    p.type = 'type'

def p_dec_vars_aux(p):
    '''dec_vars_aux : ID
                    | ID COMMA dec_vars_aux'''
    p.type = 'dec_var'

def p_functions(p):
    '''functions : functType ID LPAREN RPAREN LBRACE functBody return RBRACE 
                 | functType ID LPAREN params RPAREN LBRACE functBody return RBRACE
                 | functType ID LPAREN RPAREN LBRACE functBody return RBRACE functions
                 | functType ID LPAREN params RPAREN LBRACE functBody return RBRACE functions'''
    p.type = 'function'

def p_functType(p):
    '''functType : VOID 
                | type'''
    p.type = 'function'

def p_params(p):
    '''params : type ID
              | type ID COMMA params'''
    p.type = 'params'

def p_type(p):
    '''type : type_aux
            | type_aux LBRACKET RBRACKET
            | type_aux LBRACKET RBRACKET LBRACKET RBRACKET'''
    p.type = 'type'

def p_type_aux(p):
    '''type_aux : INT
                | FLOAT
                | CHAR
                | STRING
                | BOOL
                | ID'''
    p.type = 'type'

def p_functBody(p):
    '''functBody : statutes_aux
                | dec_vars statutes_aux'''
    p.type = 'function'

def p_return(p): 
    '''return : RETURN expression SEMICOLON
              | empty'''
    p.type = 'function'

def p_statutes(p):
    '''statutes : assignation 
                | call SEMICOLON
                | read
                | write
                | condition
                | while
                | for'''
    p.type = 'statute'

def p_assignation(p):
    'assignation : vars EQUAL expression SEMICOLON'
    p.type = 'assignation'

def p_write(p):
    'write : WRITE LPAREN write_aux RPAREN SEMICOLON'
    p.type = 'write'

def p_write_aux(p):
    '''write_aux : expression
                | expression COMMA write_aux'''
    p.type = 'write'

def p_condition(p):
    'condition : IF condition_aux'
    p.type = 'condition'

def p_condition_aux(p):
    '''condition_aux : LPAREN expression RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_2
                    | LPAREN expression RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_2 ELSE LBRACE statutes_aux RBRACE'''
    p.type = 'condition'

def p_statutes_aux(p):
    '''statutes_aux : statutes 
                    | statutes statutes_aux'''
    p.type = 'statute'

def p_condition_aux_2(p): 
    '''condition_aux_2 : ELIF condition_aux
                        | empty'''
    p.type = 'condition'

def p_while(p):
    'while : WHILE LPAREN expression RPAREN DO LBRACE statutes_aux RBRACE'
    p.type = 'while'

def p_for(p):
    'for : FROM assignation UNTIL expression DO LBRACE statutes_aux RBRACE'
    p.type = 'for'

def p_class(p):
    '''class : CLASS ID LBRACE dec_vars functions RBRACE
               | CLASS ID INHERITS ID LBRACE dec_vars functions RBRACE'''
    p.type = 'class'

def p_main(p):
    '''main : MAIN LBRACE statutes_aux RBRACE
            | MAIN LBRACE dec_vars statutes_aux RBRACE'''
    p.type = 'main'

def p_expression(p):
    '''expression : expression_aux 
                    | expression_aux RELOP expression_aux
                    | expression_aux AND expression_aux
                    | expression_aux OR expression_aux'''
    p.type = 'expression'

def p_expression_aux(p):
    '''expression_aux : call
                        | exp'''
    p.type = 'expression'

def p_call(p):
    '''call : ID LPAREN call_aux RPAREN
            | ID POINT ID LPAREN call_aux RPAREN'''
    p.type = 'call'

def p_call_aux(p):
    '''call_aux : call_aux_2 
                | empty'''
    p.type = 'call'

def p_call_aux_2(p):
    '''call_aux_2 : exp 
                | exp COMMA call_aux_2'''
    p.type = 'call'

def p_read(p):
    'read : READ LPAREN read_aux RPAREN SEMICOLON'
    p.type = 'read'

def p_read_aux(p):
    '''read_aux : vars
                | vars COMMA read_aux'''
    p.type = 'read'

def p_vars(p):
    '''vars : ID 
            | ID vars_aux'''
    p.type = 'vars'

def p_vars_aux(p): 
    '''vars_aux : LBRACKET exp RBRACKET 
                | LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''
    p.type = 'vars'

def p_exp(p):
    '''exp : term 
            | term PLUS exp
            | term MINUS exp'''
    p.type = 'exp'

def p_term(p):
    '''term : factor
                | factor TIMES term
                | factor DIVIDE term'''
    p.type = 'term'

def p_factor(p):
    '''factor :  PLUS cte 
            | MINUS cte 
            | cte 
            | LPAREN expression RPAREN'''
    p.type = 'factor'

def p_cte(p):
    '''cte : ID
            | CTEI
            | CTEF
            | CTESTRING
            | CTECHAR'''
    p.type = 'cte'

def p_empty(p):
    'empty :  '
    pass 

def p_error(p):
    print("Syntax error in:", p.type) 

# if __name__ == '__main__':

# Build parser
parser = yacc.yacc()

# Read file
doc = input()
fileData = open(doc,'r')

text = ""

for line in fileData:
    try:
        text = text + line.strip()
    except EOFError:
        break
        
if text:
    #isAccepted = parser.parse(lexer.tokenize(text))
    result = parser.parse(text)

    if result != None:
        print("Program accepted")
    else:
        print("Program failed")
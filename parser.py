# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 21/04/2021

import ply.yacc as yacc
from lexer import tokens # Get the token list from the lexer
import semanticFunc as sF

def p_program(p):
    'program : PROGRAM ID TWOPOINTS program_classes MAIN add_class LBRACE program_body init RBRACE END'
    p[0] = 'program'

def p_program_classes(p):
    '''program_classes : classes 
                        | empty'''
    p[0] = 'program'

def p_program_body(p):
    'program_body : program_body_vars program_body_funct'
    p[0] = 'program'

def p_program_body_vars(p):
    '''program_body_vars : dec_vars
                        | empty'''
    p[0] = 'program'

def p_program_body_funct(p):
    '''program_body_funct : functions 
                        | empty'''
    p[0] = 'program'

def p_dec_vars(p):
    '''dec_vars : VAR dec_vars_aux'''
    p[0] = 'program'

def p_dec_vars_aux(p):
    '''dec_vars_aux : simple_type vars_simple_type SEMICOLON
                    | simple_type vars_simple_type SEMICOLON dec_vars_aux
                    | complex_type vars_complex_type SEMICOLON
                    | complex_type vars_complex_type SEMICOLON dec_vars_aux'''
    p[0] = 'program'

def p_vars_complex_type(p):
    '''vars_complex_type : ID 
                        | ID COMMA vars_complex_type'''
    p[0] = 'program'

def p_vars_simple_type(p):
    '''vars_simple_type : ID add_variable
                        | ID add_variable COMMA vars_simple_type
                        | ID vars_simple_type_aux
                        | ID vars_simple_type_aux COMMA vars_simple_type'''
    p[0] = 'program'

def p_vars_simple_type_aux(p):
    '''vars_simple_type_aux : LBRACKET CTEI RBRACKET add_array_variable
                            | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET add_matrix_variable'''
    p[0] = 'program'

def p_simple_type(p):
    '''simple_type : INT 
                    | FLOAT 
                    | CHAR'''
    p[0] = p[1]

def p_complex_type(p):
    'complex_type : ID'
    p[0] = 'program'

def p_classes(p):
    '''classes : CLASS ID classes_aux 
                | CLASS ID classes_aux classes'''
    p[0] = 'program'

def p_classes_aux(p):
    '''classes_aux : add_class LBRACE dec_vars functions RBRACE
                    | add_class LBRACE functions RBRACE
                    | INHERITS ID add_inherit_class LBRACE dec_vars functions RBRACE
                    | INHERITS ID add_inherit_class LBRACE functions RBRACE'''
    p[0] = 'program'

def p_functions(p):
    '''functions : FUNCT functions_aux
                | FUNCT functions_aux functions'''
    p[0] = 'program'

def p_functions_aux(p):
    '''functions_aux : VOID ID add_function LPAREN params RPAREN body
                    | VOID ID add_function LPAREN RPAREN body
                    | simple_type ID add_function LPAREN RPAREN body
                    | simple_type ID add_function LPAREN params RPAREN body'''
    p[0] = 'program'

def p_params(p):
    '''params : simple_type ID add_variable
            | simple_type ID add_variable COMMA params
            | simple_type ID params_aux
            | simple_type ID params_aux COMMA params'''
    p[0] = 'program'

def p_params_aux(p):
    '''params_aux : LBRACKET RBRACKET add_array_var_params
                | LBRACKET RBRACKET LBRACKET RBRACKET add_matrix_var_params'''

def p_body(p):
    '''body : LBRACE dec_vars statutes_aux RBRACE
            | LBRACE statutes_aux RBRACE
            | LBRACE statutes_aux RETURN ID SEMICOLON RBRACE
            | LBRACE dec_vars statutes_aux RETURN ID SEMICOLON RBRACE'''
    p[0] = 'program'

def p_statutes(p):
    '''statutes : ASSIGN assignation SEMICOLON
                | CALL call SEMICOLON
                | read
                | write
                | condition
                | while
                | for'''
    p[0] = 'program'

def p_statutes_aux(p):
    '''statutes_aux : statutes
                    | statutes statutes_aux'''
    p[0] = 'program'

def p_assignation(p):
    'assignation : var EQUAL exp'
    p[0] = 'program'

def p_var(p):
    '''var : ID
            | ID var_aux'''
    p[0] = 'program'

def p_var_aux(p):
    '''var_aux : POINT ID 
            |  POINT ID var_aux_2
            |  var_aux_2'''
    p[0] = 'program'

def p_var_aux_2(p):
    '''var_aux_2 : LBRACKET exp RBRACKET
            |  LBRACKET exp RBRACKET LBRACKET exp RBRACKET'''
    p[0] = 'program'

def p_call(p):
    '''call : ID LPAREN RPAREN
            | ID POINT ID LPAREN RPAREN
            | ID LPAREN call_aux RPAREN
            | ID POINT ID LPAREN call_aux RPAREN'''
    p[0] = 'program'

def p_call_aux(p):
    '''call_aux : exp
                | exp COMMA call_aux'''
    p[0] = 'program'

def p_condition(p):
    'condition : IF condition_aux'
    p[0] = 'program'

def p_condition_aux(p):
    '''condition_aux : LPAREN exp RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_3
                    | condition_aux_2'''
    p[0] = 'program'

def p_condition_aux_2(p): 
    '''condition_aux_2 : LPAREN exp RPAREN THEN LBRACE statutes_aux RBRACE ELIF condition_aux'''
    p[0] = 'program'

def p_condition_aux_3(p):
    '''condition_aux_3 : ELSE LBRACE statutes_aux RBRACE
                        | empty'''
    p[0] = 'program'

def p_read(p):
    'read : READ LPAREN var RPAREN SEMICOLON'
    p[0] = 'program'

def p_write(p):
    '''write : WRITE LPAREN write_aux RPAREN SEMICOLON'''
    p[0] = 'program'

def p_write_aux(p):
    '''write_aux : exp
                | exp COMMA write_aux
                | CTESTRING
                | CTESTRING COMMA write_aux'''
    p[0] = 'program'

def p_while(p):
    'while : WHILE LPAREN exp RPAREN DO LBRACE statutes_aux RBRACE'
    p[0] = 'program'

def p_for(p):
    'for : FROM LPAREN assignation RPAREN UNTIL LPAREN exp RPAREN DO LBRACE statutes_aux RBRACE'
    p[0] = 'program'

def p_exp(p):
    '''exp : n_exp pop_op
            | n_exp pop_op OR push_op exp'''   
    p[0] = 'program'

def p_n_exp(p):
    '''n_exp : l_exp pop_op
            | l_exp pop_op AND push_op n_exp'''  
    p[0] = 'program'

def p_l_exp(p):
    '''l_exp : a_exp pop_op
            | a_exp pop_op RELOP push_op a_exp''' 
    p[0] = 'program'

def p_a_exp(p):
    '''a_exp : term pop_op
            | term pop_op PLUS push_op a_exp
            | term pop_op MINUS push_op a_exp'''
    p[0] = 'program'

def p_term(p):
    '''term : factor pop_op
            | factor pop_op TIMES push_op term
            | factor pop_op DIVIDE push_op term'''
    p[0] = 'program'

def p_factor(p):
    '''factor : LPAREN push_paren exp RPAREN pop_paren
            | var
            | call
            | factor_aux'''
    p[0] = 'program'

def p_factor_aux(p):
    '''factor_aux : cte
                | PLUS cte
                | MINUS cte'''
    p[0] = 'program'

def p_cte(p):
    '''cte : ID push_var
        | CTEI push_var
        | CTEF push_var
        | CTECHAR push_var'''
    p[0] = 'program'

def p_init(p):
    '''init : INIT add_init LBRACE statutes_aux RBRACE
            | INIT add_init LBRACE dec_vars statutes_aux RBRACE'''
    p[0] = 'program'

def p_empty(p):
    'empty :'
    pass 

def p_error(p):
    print("Syntax error in:", p.type) 

# FUNCTIONS TO CREATE DICTIONARIES

def p_add_variable(p):
    'add_variable :'
    sF.addVars(p[-1], p[-2], 0, 0)
    p[0] = 'program'

def p_add_array_variable(p):
    'add_array_variable :'
    sF.addVars(p[-4], p[-5], p[-2], 0)
    p[0] = 'program'

def p_add_matrix_variable(p):
    'add_matrix_variable :'
    sF.addVars(p[-7], p[-8], p[-5], p[-2])
    p[0] = 'program'

def p_add_array_var_params(p):
    'add_array_var_params :'
    sF.addVars(p[-3], p[-4], 0, 0)
    p[0] = 'program'

def p_add_matrix_var_params(p):
    'add_matrix_var_params :'
    sF.addVars(p[-5], p[-6], 0, 0)
    p[0] = 'program'

def p_add_function(p):
    'add_function :'
    sF.addFunction(p[-1], p[-2])

def p_add_init(p):
    'add_init :'
    sF.addFunction(p[-1], "void")

def p_add_class(p):
    'add_class :'
    sF.addClass(p[-1], False, None)

def p_add_inherit_class(p):
    'add_inherit_class :'
    sF.addClass(p[-3], True, p[-1])

# FUNCTIONS FOR EXPRESSIONS

def p_push_var(p):
    'push_var :'
    sF.pushVar(p[-1])

def p_push_op(p):
    'push_op :'
    sF.pushOp(p[-1])

def p_pop_op(p):
    'pop_op :'
    sF.popOp()

def p_push_paren(p):
    'push_paren :'
    sF.pushParen(p[-1])

def p_pop_paren(p):
    'pop_paren :'
    sF.popParen()


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
    result = parser.parse(text)

    if result != None:
        print("Program accepted")
    else:
        print("Program failed")
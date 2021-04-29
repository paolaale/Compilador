# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 30/04/2021

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
    '''dec_vars_aux : dec_vars_simple
                    | dec_vars_complex'''
    p[0] = 'program'

def p_dec_vars_simple(p):
    '''dec_vars_simple : simple_type vars_simple_type SEMICOLON
                            | simple_type vars_simple_type SEMICOLON dec_vars_aux'''
    p[0] = 'program'

def p_simple_type(p):
    '''simple_type : INT 
                    | FLOAT 
                    | CHAR'''
    p[0] = p[1]
    
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

def p_dec_vars_complex(p):
    '''dec_vars_complex : OBJECT vars_complex_type SEMICOLON
                              | OBJECT vars_complex_type SEMICOLON dec_vars_aux'''
    p[0] = 'program'

def p_vars_complex_type(p):
    '''vars_complex_type : ID add_variable
                         | ID add_variable COMMA vars_complex_type'''
    p[0] = 'program'

def p_classes(p):
    '''classes : CLASS OBJECT classes_aux 
                | CLASS OBJECT classes_aux classes'''
    p[0] = 'program'

def p_classes_aux(p):
    '''classes_aux : add_class LBRACE dec_vars functions RBRACE
                    | add_class LBRACE functions RBRACE
                    | INHERITS OBJECT add_inherit_class LBRACE dec_vars functions RBRACE
                    | INHERITS OBJECT add_inherit_class LBRACE functions RBRACE'''
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
    '''statutes : assignation SEMICOLON
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
    '''assignation : ID push_var EQUAL push_op exp pop_op_assign
                    | ID var_aux push_var EQUAL push_op exp pop_op_assign'''
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
    'condition : IF LPAREN exp RPAREN if_condition THEN LBRACE statutes_aux RBRACE condition_aux_elif condition_aux_else end_if'
    p[0] = 'program'

def p_condition_aux_elif(p): 
    '''condition_aux_elif : ELIF LPAREN elif_expression exp RPAREN elif_condition THEN LBRACE statutes_aux RBRACE condition_aux_elif
                        | empty'''
    p[0] = 'program'

def p_condition_aux_else(p):
    '''condition_aux_else : ELSE else_condition LBRACE statutes_aux RBRACE
                        | empty'''
    p[0] = 'program'

def p_read(p):
    'read : READ LPAREN read_aux RPAREN SEMICOLON generate_read'
    p[0] = 'program'

def p_read_aux(p):
    '''read_aux : ID push_var
            | ID push_var COMMA generate_read read_aux'''
    p[0] = 'program'

def p_write(p):
    '''write : WRITE LPAREN write_aux RPAREN SEMICOLON generate_write'''
    p[0] = 'program'

def p_write_aux(p):
    '''write_aux : exp
                | exp COMMA generate_write write_aux
                | CTESTRING save_string
                | CTESTRING save_string COMMA generate_write write_aux'''
    p[0] = 'program'

def p_while(p):
    'while : WHILE push_while_jump LPAREN exp RPAREN generate_while_quad DO LBRACE statutes_aux RBRACE define_while_jumps'
    p[0] = 'program'

def p_for(p):
    'for : FROM LPAREN assignation RPAREN UNTIL LPAREN exp RPAREN DO LBRACE statutes_aux RBRACE'
    p[0] = 'program'

def p_exp(p):
    '''exp : l_exp pop_op_lop
            | l_exp pop_op_lop OR push_op exp
            | l_exp pop_op_lop AND push_op exp'''   
    p[0] = 'program'

def p_l_exp(p):
    '''l_exp : a_exp 
            | a_exp RELOP push_op a_exp pop_op_relop''' 
    p[0] = 'program'

def p_a_exp(p):
    '''a_exp : term pop_op_art_n2
            | term pop_op_art_n2 PLUS push_op a_exp
            | term pop_op_art_n2 MINUS push_op a_exp'''
    p[0] = 'program'

def p_term(p):
    '''term : factor pop_op_art_n1
            | factor pop_op_art_n1 TIMES push_op term
            | factor pop_op_art_n1 DIVIDE push_op term'''
    p[0] = 'program'

def p_factor(p):
    '''factor : LPAREN push_paren exp RPAREN pop_paren
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
        | ID var_aux push_var
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
    sF.pushOperand(p[-1])

def p_push_op(p):
    'push_op :'
    sF.pushOperator(p[-1])

def p_pop_op_art_n1(self):
    'pop_op_art_n1 :'
    sF.pop_op_art_n1()

def p_pop_op_art_n2(self):
    'pop_op_art_n2 :'
    sF.pop_op_art_n2()

def p_pop_op_relop(self):
    'pop_op_relop :'
    sF.pop_op_relop()

def p_pop_op_lop(self):
    'pop_op_lop :'
    sF.pop_op_lop()

def p_pop_op_assign(self):
    'pop_op_assign :'
    sF.pop_op_assign()

def p_push_paren(p):
    'push_paren :'
    sF.pushOperator(p[-1])

def p_pop_paren(p):
    'pop_paren :'
    sF.pop_paren()

def p_generate_write(self):
    'generate_write :'
    sF.generateWrite()

def p_save_string(p):
    'save_string :'
    sF.saveString(p[-1])

def p_generate_read(self):
    'generate_read :'
    sF.generateRead()

# Functions for NO-LINEAL statements

def p_if_condition(self):
    'if_condition :'
    sF.ifCondition()

def p_elif_condition(self):
    'elif_condition :'
    sF.elifCondition()

def p_elif_expression(self):
    'elif_expression :'
    sF.elifExpression()

def p_else_condition(self):
    'else_condition :'
    sF.elseCondition()

def p_end_if(self):
    'end_if :'
    sF.endIF()

def p_push_while_jump(self):
    'push_while_jump :'
    sF.pushWhileJump()

def p_generate_while_quad(self):
    'generate_while_quad :'
    sF.generateWhileQuad()

def p_define_while_jumps(self):
    'define_while_jumps :'
    sF.defineWhileJumps()

if __name__ == '__main__':
    
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

        print("stack of operands: ", sF.operandsStack)
        print("stack of operators: ", sF.operatorsStack)
        print("stack of types: ", sF.typesStack)
        print("stack of jumps: ", sF.jumpsStack)
        sF.printQuadruples()

        if result != None:
            print("Program accepted")
        else:
            print("Program failed")
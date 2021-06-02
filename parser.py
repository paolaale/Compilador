# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 02/06/2021

import ply.yacc as yacc
from lexer import tokens # Get the token list from the lexer
import semanticFunc as sF


def p_program(p):
    'program : PROGRAM ID TWOPOINTS check_init program_classes MAIN add_class LBRACE program_body init RBRACE END end_program'
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
    '''functions_aux : VOID ID add_function LPAREN params RPAREN insert_number_params body
                    | VOID ID add_function LPAREN RPAREN body
                    | simple_type ID add_function LPAREN RPAREN body
                    | simple_type ID add_function LPAREN params RPAREN insert_number_params body'''
    p[0] = 'program'

def p_params(p):
    '''params : simple_type ID add_param
            | simple_type ID add_param COMMA params'''
    p[0] = 'program'

def p_body(p):
    '''body : LBRACE start_function dec_vars statutes_aux RBRACE end_function
            | LBRACE start_function statutes_aux RBRACE end_function
            | LBRACE start_function statutes_aux RETURN ID return_function SEMICOLON RBRACE end_function
            | LBRACE start_function dec_vars statutes_aux RETURN ID return_function SEMICOLON RBRACE end_function
            | LBRACE start_function RETURN ID return_function SEMICOLON RBRACE end_function'''
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
                    | ID var_aux EQUAL push_op exp pop_op_assign
                    | ID push_var var_aux_2 EQUAL push_op exp pop_op_assign'''
    p[0] = 'program'

def p_var_aux(p):
    '''var_aux : POINT ID push_obj_var
            |  POINT ID var_aux_2'''
    p[0] = 'program'

def p_var_aux_2(p):
    '''var_aux_2 : LBRACKET access_array exp verify_array_index RBRACKET var_aux_3'''
    p[0] = 'program'

def p_var_aux_3(p):
    '''var_aux_3 : LBRACKET access_matrix exp verify_matrix_index RBRACKET end_matrix
                | end_array'''
    p[0] = 'program'

def p_call(p):
    '''call : ID exist_function LPAREN era_function RPAREN gosub_function
            | ID POINT ID exist_method LPAREN era_method RPAREN gosub_method
            | ID exist_function LPAREN push_paren era_function call_aux RPAREN pop_paren gosub_function
            | ID POINT ID exist_method LPAREN push_paren era_method call_aux_2 RPAREN pop_paren gosub_method'''
    p[0] = 'program'

def p_call_aux(p):
    '''call_aux : exp arg_function
                | exp arg_function COMMA call_aux'''

    p[0] = 'program'

def p_call_aux_2(p):
    '''call_aux_2 : exp arg_method
                | exp arg_method COMMA call_aux_2'''
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
            | ID push_var COMMA generate_read read_aux 
            | ID var_aux
            | ID var_aux COMMA generate_read read_aux
            | ID push_var var_aux_2
            | ID push_var var_aux_2 COMMA generate_read read_aux'''
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
    'while : WHILE while_jump LPAREN exp RPAREN while_condition DO LBRACE statutes_aux RBRACE end_while'
    p[0] = 'program'

def p_for(p):
    'for : FROM LPAREN assignation RPAREN UNTIL for_jump LPAREN exp RPAREN for_condition DO LBRACE statutes_aux RBRACE end_for'
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
            | factor_aux
            | call'''
    p[0] = 'program'

def p_factor_aux(p):
    '''factor_aux : cte
                | PLUS cte
                | MINUS cte'''
    p[0] = 'program'

def p_cte(p):
    '''cte : ID push_var 
        | ID var_aux
        | ID push_var var_aux_2
        | CTEI push_var
        | CTEF push_var
        | CTECHAR push_var'''
    p[0] = 'program'

def p_init(p):
    '''init : INIT add_init LBRACE start_init statutes_aux RBRACE
            | INIT add_init LBRACE start_init dec_vars statutes_aux RBRACE'''
    p[0] = 'program'

def p_empty(p):
    'empty :'
    pass 

def p_error(p):
    print("Syntax error in:", p.type) 

# FUNCTIONS TO CREATE DICTIONARIES

def p_add_variable(p):
    'add_variable :'
    sF.addVars(p[-1], p[-2], -1, -1)

def p_add_array_variable(p):
    'add_array_variable :'
    sF.addVars(p[-4], p[-5], p[-2], -1)

def p_add_matrix_variable(p):
    'add_matrix_variable :'
    sF.addVars(p[-7], p[-8], p[-5], p[-2])

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

def p_push_obj_var(p):
    'push_obj_var :'
    sF.pushObjVar(p[-3], p[-1])

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

# FUNCTIONS FOR LINEAL STATEMENTS

def p_generate_write(self):
    'generate_write :'
    sF.generateWrite()

def p_save_string(p):
    'save_string :'
    sF.saveString(p[-1])

def p_generate_read(self):
    'generate_read :'
    sF.generateRead()

# FUNCTIONS FOR NO-LINEAL STATEMENTS

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

def p_while_jump(self):
    'while_jump :'
    sF.whileJump()

def p_while_condition(self):
    'while_condition :'
    sF.whileCondition()

def p_end_while(self):
    'end_while :'
    sF.endWhile()

def p_for_jump(self):
    'for_jump :'
    sF.forJump()

def p_for_condition(self):
    'for_condition :'
    sF.forCondition()

def p_end_for(self):
    'end_for :'
    sF.endFor()

# FUNCTION FOR FUNTCIONS

def p_add_param(p):
    'add_param :'
    sF.addParam(p[-1], p[-2], -1, -1)

def p_insert_number_params(self):
    'insert_number_params :'
    sF.insertParams()

def p_start_function(self):
    'start_function :'
    sF.startFunction() 

def p_return_function(p):
    'return_function :'
    sF.returnFunction(p[-1])
    
def p_end_function(self):
    'end_function :'
    sF.endFunction()

def p_exist_function(p):
    'exist_function :'
    sF.existFunction(p[-1])

def p_era_function(self):
    'era_function :'
    sF.eraSizeFunction()

def p_arg_function(self):
    'arg_function :'
    sF.argFunction()

def p_gosub_function(self):
    'gosub_function :'
    sF.gosubFunction()

# FUNCTIONS FOR ARRAYS

def p_access_array(self):
    'access_array :'
    sF.accessArray()

def p_verify_array_index(self):
    'verify_array_index :'
    sF.verifyArrayIndex()

def p_end_array(self):
    'end_array :'
    sF.endArray()

def p_access_matrix(self):
    'access_matrix :'
    sF.accessMatrix()

def p_verify_matrix_index(self):
    'verify_matrix_index :'
    sF.verifyMatrixIndex()

def p_end_matrix(self):
    'end_matrix :'
    sF.endMatrix()

# FUNCTIONS FOR CLASSES

def p_exist_method(p):
    'exist_method :'
    sF.existMethod(p[-3], p[-1])

def p_era_method(self):
    'era_method :'
    sF.eraSizeMethod()

def p_arg_method(self):
    'arg_method :'
    sF.argMethod()

def p_gosub_method(self):
    'gosub_method :'
    sF.gosubMethod()

# FUNCTIONS FOR MAIN

def p_check_init(self):
    'check_init :'
    sF.checkInit()

def p_start_init(self):
    'start_init :'
    sF.startInit()

# FUNCTION FOR END

def p_end_program(self):
    'end_program :'
    sF.endProgram()

# Build parser
parser = yacc.yacc()
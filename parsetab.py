
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND CALL CHAR CLASS COMMA CTECHAR CTEF CTEI CTESTRING DIVIDE DO ELIF ELSE END EQUAL FLOAT FROM FUNCT ID IF INHERITS INIT INT LBRACE LBRACKET LPAREN MAIN MINUS OBJECT OR PLUS POINT PROGRAM RBRACE RBRACKET READ RELOP RETURN RPAREN SEMICOLON THEN TIMES TWOPOINTS UNTIL VAR VOID WHILE WRITEprogram : PROGRAM ID TWOPOINTS check_init program_classes MAIN add_class LBRACE program_body init RBRACE END end_programprogram_classes : classes \n                        | emptyprogram_body : program_body_vars program_body_functprogram_body_vars : dec_vars\n                        | emptyprogram_body_funct : functions \n                        | emptydec_vars : VAR dec_vars_auxdec_vars_aux : dec_vars_simple\n                    | dec_vars_complexdec_vars_simple : simple_type vars_simple_type SEMICOLON\n                        | simple_type vars_simple_type SEMICOLON dec_vars_auxsimple_type : INT \n                    | FLOAT \n                    | CHARvars_simple_type : ID add_variable\n                        | ID add_variable COMMA vars_simple_type\n                        | ID vars_simple_type_aux\n                        | ID vars_simple_type_aux COMMA vars_simple_typevars_simple_type_aux : LBRACKET CTEI RBRACKET add_array_variable\n                            | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET add_matrix_variabledec_vars_complex : OBJECT vars_complex_type SEMICOLON\n                              | OBJECT vars_complex_type SEMICOLON dec_vars_auxvars_complex_type : ID add_variable\n                         | ID add_variable COMMA vars_complex_typeclasses : CLASS OBJECT classes_aux \n                | CLASS OBJECT classes_aux classesclasses_aux : add_class LBRACE dec_vars functions RBRACE\n                    | add_class LBRACE functions RBRACE\n                    | INHERITS OBJECT add_inherit_class LBRACE dec_vars functions RBRACE\n                    | INHERITS OBJECT add_inherit_class LBRACE functions RBRACEfunctions : FUNCT functions_aux\n                | FUNCT functions_aux functionsfunctions_aux : VOID ID add_function LPAREN params RPAREN insert_number_params body\n                    | VOID ID add_function LPAREN RPAREN body\n                    | simple_type ID add_function LPAREN RPAREN body\n                    | simple_type ID add_function LPAREN params RPAREN insert_number_params bodyparams : simple_type ID add_param\n            | simple_type ID add_param COMMA params\n            | simple_type ID params_aux\n            | simple_type ID params_aux COMMA paramsparams_aux : LBRACKET RBRACKET add_array_var_params\n                | LBRACKET RBRACKET LBRACKET RBRACKET add_matrix_var_paramsbody : LBRACE start_function dec_vars statutes_aux RBRACE end_function\n            | LBRACE start_function statutes_aux RBRACE end_function\n            | LBRACE start_function statutes_aux RETURN ID return_function SEMICOLON RBRACE end_function\n            | LBRACE start_function dec_vars statutes_aux RETURN ID return_function SEMICOLON RBRACE end_functionstatutes : assignation SEMICOLON\n                | CALL call SEMICOLON\n                | read\n                | write\n                | condition\n                | while\n                | forstatutes_aux : statutes\n                    | statutes statutes_auxassignation : ID push_var EQUAL push_op exp pop_op_assign\n                    | ID var_aux push_var EQUAL push_op exp pop_op_assignvar_aux : POINT ID \n            |  POINT ID var_aux_2\n            |  var_aux_2var_aux_2 : LBRACKET exp RBRACKET\n            |  LBRACKET exp RBRACKET LBRACKET exp RBRACKETcall : ID  exist_function LPAREN era_function RPAREN gosub_function\n            | ID POINT ID LPAREN RPAREN\n            | ID exist_function LPAREN era_function call_aux RPAREN gosub_function\n            | ID POINT ID LPAREN call_aux RPARENcall_aux : exp arg_function\n                | exp arg_function COMMA call_auxcondition : IF LPAREN exp RPAREN if_condition THEN LBRACE statutes_aux RBRACE condition_aux_elif condition_aux_else end_ifcondition_aux_elif : ELIF LPAREN elif_expression exp RPAREN elif_condition THEN LBRACE statutes_aux RBRACE condition_aux_elif\n                        | emptycondition_aux_else : ELSE else_condition LBRACE statutes_aux RBRACE\n                        | emptyread : READ LPAREN read_aux RPAREN SEMICOLON generate_readread_aux : ID push_var\n            | ID push_var COMMA generate_read read_auxwrite : WRITE LPAREN write_aux RPAREN SEMICOLON generate_writewrite_aux : exp\n                | exp COMMA generate_write write_aux\n                | CTESTRING save_string\n                | CTESTRING save_string COMMA generate_write write_auxwhile : WHILE while_jump LPAREN exp RPAREN while_condition DO LBRACE statutes_aux RBRACE end_whilefor : FROM LPAREN assignation RPAREN UNTIL for_jump LPAREN exp RPAREN for_condition DO LBRACE statutes_aux RBRACE end_forexp : l_exp pop_op_lop\n            | l_exp pop_op_lop OR push_op exp\n            | l_exp pop_op_lop AND push_op expl_exp : a_exp \n            | a_exp RELOP push_op a_exp pop_op_relopa_exp : term pop_op_art_n2\n            | term pop_op_art_n2 PLUS push_op a_exp\n            | term pop_op_art_n2 MINUS push_op a_expterm : factor pop_op_art_n1\n            | factor pop_op_art_n1 TIMES push_op term\n            | factor pop_op_art_n1 DIVIDE push_op termfactor : LPAREN push_paren exp RPAREN pop_paren\n            | call\n            | factor_auxfactor_aux : cte\n                | PLUS cte\n                | MINUS ctecte : ID push_var\n        | ID var_aux push_var\n        | CTEI push_var\n        | CTEF push_var\n        | CTECHAR push_varinit : INIT add_init LBRACE start_init statutes_aux RBRACE\n            | INIT add_init LBRACE start_init dec_vars statutes_aux RBRACEempty :add_variable :add_array_variable :add_matrix_variable :add_function :add_init :add_class :add_inherit_class :push_var :push_op :pop_op_art_n1 :pop_op_art_n2 :pop_op_relop :pop_op_lop :pop_op_assign :push_paren :pop_paren :generate_write :save_string :generate_read :if_condition :elif_condition :elif_expression :else_condition :end_if :while_jump :while_condition :end_while :for_jump :for_condition :end_for :add_param :add_array_var_params :add_matrix_var_params :insert_number_params :start_function :return_function :end_function :exist_function :era_function :arg_function :gosub_function :check_init :start_init :end_program :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,60,72,],[0,-154,-1,]),'ID':([2,34,35,36,37,38,39,40,41,45,46,61,62,66,73,74,75,76,78,79,84,85,87,88,89,90,91,92,105,111,116,118,119,120,121,123,128,133,135,136,143,144,146,160,164,169,171,172,176,182,183,192,199,205,206,208,209,210,211,212,213,214,215,216,220,221,222,223,224,231,244,245,247,248,249,250,252,253,254,256,261,281,283,289,291,296,301,303,304,308,310,311,312,315,317,318,319,324,325,327,329,331,332,],[3,-9,-10,-11,51,53,-14,-15,-16,56,57,-153,-12,-23,93,-13,51,51,-24,53,93,93,113,-51,-52,-53,-54,-55,129,-49,138,149,155,149,149,93,-145,-50,170,-119,179,179,-125,149,93,-149,149,-119,-119,149,218,-127,93,149,149,149,149,-119,-119,149,-119,-119,-119,-119,-129,-129,-127,149,-127,263,149,149,149,149,149,149,-76,155,-79,149,285,93,149,149,93,-110,-110,-73,-137,-134,-75,-132,-84,-71,149,93,93,-140,-74,-85,93,-110,-72,]),'TWOPOINTS':([3,],[4,]),'CLASS':([4,5,13,43,54,71,82,],[-152,9,9,-30,-29,-32,-31,]),'MAIN':([4,5,6,7,8,13,17,43,54,71,82,],[-152,-110,10,-2,-3,-27,-28,-30,-29,-32,-31,]),'OBJECT':([9,15,24,62,66,],[11,19,38,38,38,]),'LBRACE':([10,11,12,14,19,28,30,49,104,106,126,131,163,168,257,282,309,313,316,328,],[-116,-116,16,18,-117,47,-115,61,128,128,-144,-144,128,128,281,291,-133,318,319,329,]),'INHERITS':([11,],[15,]),'VAR':([16,18,47,61,73,128,164,],[24,24,24,-153,24,-145,24,]),'FUNCT':([16,18,21,22,23,25,34,35,36,44,47,58,62,66,74,78,127,130,198,204,230,260,262,284,300,306,307,314,],[-110,27,27,-5,-6,27,-9,-10,-11,27,27,27,-12,-23,-13,-24,-36,-37,-35,-38,-147,-147,-46,-45,-147,-147,-47,-48,]),'INIT':([16,20,21,22,23,31,32,33,34,35,36,44,55,62,66,74,78,127,130,198,204,230,260,262,284,300,306,307,314,],[-110,30,-110,-5,-6,-4,-7,-8,-9,-10,-11,-33,-34,-12,-23,-13,-24,-36,-37,-35,-38,-147,-147,-46,-45,-147,-147,-47,-48,]),'INT':([24,27,62,66,80,81,201,202,],[39,39,39,39,39,39,39,39,]),'FLOAT':([24,27,62,66,80,81,201,202,],[40,40,40,40,40,40,40,40,]),'CHAR':([24,27,62,66,80,81,201,202,],[41,41,41,41,41,41,41,41,]),'RBRACE':([26,29,42,44,55,59,70,83,85,88,89,90,91,92,108,109,110,111,127,130,132,133,198,200,204,220,222,229,230,252,254,260,262,284,290,294,296,297,299,300,301,303,304,306,307,308,310,312,314,315,321,322,324,325,327,330,331,332,],[43,48,54,-33,-34,71,82,108,-56,-51,-52,-53,-54,-55,-108,132,-57,-49,-36,-37,-109,-50,-35,230,-38,-129,-127,260,-147,-76,-79,-147,-46,-45,296,300,-110,304,306,-147,-110,-73,-137,-147,-47,-134,-75,-84,-48,-71,324,325,-140,-74,-85,331,-110,-72,]),'VOID':([27,],[45,]),'CALL':([34,35,36,61,62,66,73,74,78,84,85,88,89,90,91,92,111,128,133,164,199,220,222,252,254,281,291,296,301,303,304,308,310,312,315,318,319,324,325,327,329,331,332,],[-9,-10,-11,-153,-12,-23,87,-13,-24,87,87,-51,-52,-53,-54,-55,-49,-145,-50,87,87,-129,-127,-76,-79,87,87,-110,-110,-73,-137,-134,-75,-84,-71,87,87,-140,-74,-85,87,-110,-72,]),'READ':([34,35,36,61,62,66,73,74,78,84,85,88,89,90,91,92,111,128,133,164,199,220,222,252,254,281,291,296,301,303,304,308,310,312,315,318,319,324,325,327,329,331,332,],[-9,-10,-11,-153,-12,-23,94,-13,-24,94,94,-51,-52,-53,-54,-55,-49,-145,-50,94,94,-129,-127,-76,-79,94,94,-110,-110,-73,-137,-134,-75,-84,-71,94,94,-140,-74,-85,94,-110,-72,]),'WRITE':([34,35,36,61,62,66,73,74,78,84,85,88,89,90,91,92,111,128,133,164,199,220,222,252,254,281,291,296,301,303,304,308,310,312,315,318,319,324,325,327,329,331,332,],[-9,-10,-11,-153,-12,-23,95,-13,-24,95,95,-51,-52,-53,-54,-55,-49,-145,-50,95,95,-129,-127,-76,-79,95,95,-110,-110,-73,-137,-134,-75,-84,-71,95,95,-140,-74,-85,95,-110,-72,]),'IF':([34,35,36,61,62,66,73,74,78,84,85,88,89,90,91,92,111,128,133,164,199,220,222,252,254,281,291,296,301,303,304,308,310,312,315,318,319,324,325,327,329,331,332,],[-9,-10,-11,-153,-12,-23,96,-13,-24,96,96,-51,-52,-53,-54,-55,-49,-145,-50,96,96,-129,-127,-76,-79,96,96,-110,-110,-73,-137,-134,-75,-84,-71,96,96,-140,-74,-85,96,-110,-72,]),'WHILE':([34,35,36,61,62,66,73,74,78,84,85,88,89,90,91,92,111,128,133,164,199,220,222,252,254,281,291,296,301,303,304,308,310,312,315,318,319,324,325,327,329,331,332,],[-9,-10,-11,-153,-12,-23,97,-13,-24,97,97,-51,-52,-53,-54,-55,-49,-145,-50,97,97,-129,-127,-76,-79,97,97,-110,-110,-73,-137,-134,-75,-84,-71,97,97,-140,-74,-85,97,-110,-72,]),'FROM':([34,35,36,61,62,66,73,74,78,84,85,88,89,90,91,92,111,128,133,164,199,220,222,252,254,281,291,296,301,303,304,308,310,312,315,318,319,324,325,327,329,331,332,],[-9,-10,-11,-153,-12,-23,98,-13,-24,98,98,-51,-52,-53,-54,-55,-49,-145,-50,98,98,-129,-127,-76,-79,98,98,-110,-110,-73,-137,-134,-75,-84,-71,98,98,-140,-74,-85,98,-110,-72,]),'END':([48,],[60,]),'SEMICOLON':([50,51,52,53,63,64,67,86,99,100,101,102,112,117,125,138,140,141,142,145,147,148,149,150,151,152,153,173,174,175,177,178,179,180,181,184,185,186,187,188,189,191,197,207,218,219,228,236,239,241,242,246,251,263,265,266,268,269,270,271,272,273,274,275,276,277,278,285,286,288,293,],[62,-111,66,-111,-17,-19,-25,111,-18,-20,-112,-26,133,-62,-21,-60,-123,-89,-121,-120,-98,-99,-118,-100,-118,-118,-118,-61,-63,-86,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,220,222,-113,-124,-60,-104,-22,-151,-66,-58,-124,-122,-126,-146,-65,-151,-68,-59,-64,-87,-88,-90,-92,-93,-95,-96,-97,-146,294,-67,299,]),'COMMA':([51,53,63,64,67,101,117,125,129,138,140,141,142,145,147,148,149,150,151,152,153,155,157,158,165,166,173,174,175,177,178,179,180,181,184,185,186,187,188,190,193,197,203,218,219,228,235,236,238,239,246,251,264,265,266,267,268,270,271,272,273,274,275,276,277,278,287,288,],[-111,-111,75,76,79,-112,-62,-21,-141,-60,-123,-89,-121,-120,-98,-99,-118,-100,-118,-118,-118,-118,192,-128,201,202,-61,-63,-86,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,221,224,-113,-142,-60,-104,-22,-43,-151,-150,-66,-122,-126,-143,-65,-151,289,-68,-64,-87,-88,-90,-92,-93,-95,-96,-97,-44,-67,]),'LBRACKET':([51,93,101,129,138,149,174,179,203,218,],[65,118,124,167,118,118,209,118,234,118,]),'LPAREN':([56,57,68,69,94,95,96,97,98,113,118,120,121,122,134,136,146,149,160,169,170,171,172,176,182,192,205,206,208,209,210,211,212,213,214,215,216,218,223,224,227,244,245,247,248,249,250,256,259,283,289,302,311,317,],[-114,-114,80,81,119,120,121,-135,123,-148,146,146,146,160,169,-119,-125,-148,146,-149,206,146,-119,-119,146,-127,146,146,146,146,-119,-119,146,-119,-119,-119,-119,206,146,-127,-138,146,146,146,146,146,146,146,283,146,146,311,-132,146,]),'CTEI':([65,118,120,121,124,136,143,144,146,160,169,171,172,176,182,192,205,206,208,209,210,211,212,213,214,215,216,223,224,244,245,247,248,249,250,256,283,289,311,317,],[77,151,151,151,162,-119,151,151,-125,151,-149,151,-119,-119,151,-127,151,151,151,151,-119,-119,151,-119,-119,-119,-119,151,-127,151,151,151,151,151,151,151,151,151,-132,151,]),'RBRACKET':([77,117,138,139,140,141,142,145,147,148,149,150,151,152,153,162,167,173,174,175,177,178,179,180,181,184,185,186,187,188,218,219,234,236,239,243,246,251,265,266,268,270,271,272,273,274,275,276,277,278,288,],[101,-62,-60,174,-123,-89,-121,-120,-98,-99,-118,-100,-118,-118,-118,197,203,-61,-63,-86,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,-60,-104,264,-151,-66,270,-122,-126,-65,-151,-68,-64,-87,-88,-90,-92,-93,-95,-96,-97,-67,]),'RPAREN':([80,81,103,107,117,129,138,140,141,142,145,147,148,149,150,151,152,153,154,155,156,157,158,159,161,165,166,169,173,174,175,177,178,179,180,181,184,185,186,187,188,190,193,195,203,205,206,207,217,218,219,232,233,235,236,237,238,239,240,241,242,246,251,255,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,287,288,292,295,320,],[104,106,126,131,-62,-141,-60,-123,-89,-121,-120,-98,-99,-118,-100,-118,-118,-118,189,-118,191,-80,-128,194,196,-39,-41,-149,-61,-63,-86,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,-77,-82,226,-142,236,239,-124,251,-60,-104,-40,-42,-43,-151,266,-150,-66,268,-58,-124,-122,-126,-81,-143,-65,-151,-69,-68,-59,-64,-87,-88,-90,-92,-93,-95,-96,-97,-78,-83,-44,-67,298,-70,323,]),'RETURN':([85,88,89,90,91,92,110,111,133,200,220,222,229,252,254,296,301,303,304,308,310,312,315,324,325,327,331,332,],[-56,-51,-52,-53,-54,-55,-57,-49,-50,231,-129,-127,261,-76,-79,-110,-110,-73,-137,-134,-75,-84,-71,-140,-74,-85,-110,-72,]),'EQUAL':([93,114,115,117,137,138,173,174,270,],[-118,136,-118,-62,172,-60,-61,-63,-64,]),'POINT':([93,113,149,179,],[116,135,183,116,]),'TIMES':([117,138,145,147,148,149,150,151,152,153,173,174,178,179,180,181,184,185,186,187,188,218,219,236,239,251,265,266,268,270,278,288,],[-62,-60,-120,-98,-99,-118,-100,-118,-118,-118,-61,-63,-101,-118,-102,215,-103,-118,-105,-106,-107,-60,-104,-151,-66,-126,-65,-151,-68,-64,-97,-67,]),'DIVIDE':([117,138,145,147,148,149,150,151,152,153,173,174,178,179,180,181,184,185,186,187,188,218,219,236,239,251,265,266,268,270,278,288,],[-62,-60,-120,-98,-99,-118,-100,-118,-118,-118,-61,-63,-101,-118,-102,216,-103,-118,-105,-106,-107,-60,-104,-151,-66,-126,-65,-151,-68,-64,-97,-67,]),'PLUS':([117,118,120,121,136,138,142,145,146,147,148,149,150,151,152,153,160,169,171,172,173,174,176,177,178,179,180,181,182,184,185,186,187,188,192,205,206,208,209,210,211,212,213,214,215,216,218,219,223,224,236,239,244,245,247,248,249,250,251,256,265,266,268,270,276,277,278,283,288,289,311,317,],[-62,143,143,143,-119,-60,-121,-120,-125,-98,-99,-118,-100,-118,-118,-118,143,-149,143,-119,-61,-63,-119,213,-101,-118,-102,-94,143,-103,-118,-105,-106,-107,-127,143,143,143,143,-119,-119,143,-119,-119,-119,-119,-60,-104,143,-127,-151,-66,143,143,143,143,143,143,-126,143,-65,-151,-68,-64,-95,-96,-97,143,-67,143,-132,143,]),'MINUS':([117,118,120,121,136,138,142,145,146,147,148,149,150,151,152,153,160,169,171,172,173,174,176,177,178,179,180,181,182,184,185,186,187,188,192,205,206,208,209,210,211,212,213,214,215,216,218,219,223,224,236,239,244,245,247,248,249,250,251,256,265,266,268,270,276,277,278,283,288,289,311,317,],[-62,144,144,144,-119,-60,-121,-120,-125,-98,-99,-118,-100,-118,-118,-118,144,-149,144,-119,-61,-63,-119,214,-101,-118,-102,-94,144,-103,-118,-105,-106,-107,-127,144,144,144,144,-119,-119,144,-119,-119,-119,-119,-60,-104,144,-127,-151,-66,144,144,144,144,144,144,-126,144,-65,-151,-68,-64,-95,-96,-97,144,-67,144,-132,144,]),'RELOP':([117,138,141,142,145,147,148,149,150,151,152,153,173,174,177,178,179,180,181,184,185,186,187,188,218,219,236,239,251,265,266,268,270,274,275,276,277,278,288,],[-62,-60,176,-121,-120,-98,-99,-118,-100,-118,-118,-118,-61,-63,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,-60,-104,-151,-66,-126,-65,-151,-68,-64,-92,-93,-95,-96,-97,-67,]),'OR':([117,138,140,141,142,145,147,148,149,150,151,152,153,173,174,175,177,178,179,180,181,184,185,186,187,188,218,219,236,239,246,251,265,266,268,270,273,274,275,276,277,278,288,],[-62,-60,-123,-89,-121,-120,-98,-99,-118,-100,-118,-118,-118,-61,-63,210,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,-60,-104,-151,-66,-122,-126,-65,-151,-68,-64,-90,-92,-93,-95,-96,-97,-67,]),'AND':([117,138,140,141,142,145,147,148,149,150,151,152,153,173,174,175,177,178,179,180,181,184,185,186,187,188,218,219,236,239,246,251,265,266,268,270,273,274,275,276,277,278,288,],[-62,-60,-123,-89,-121,-120,-98,-99,-118,-100,-118,-118,-118,-61,-63,211,-91,-101,-118,-102,-94,-103,-118,-105,-106,-107,-60,-104,-151,-66,-122,-126,-65,-151,-68,-64,-90,-92,-93,-95,-96,-97,-67,]),'CTEF':([118,120,121,136,143,144,146,160,169,171,172,176,182,192,205,206,208,209,210,211,212,213,214,215,216,223,224,244,245,247,248,249,250,256,283,289,311,317,],[152,152,152,-119,152,152,-125,152,-149,152,-119,-119,152,-127,152,152,152,152,-119,-119,152,-119,-119,-119,-119,152,-127,152,152,152,152,152,152,152,152,152,-132,152,]),'CTECHAR':([118,120,121,136,143,144,146,160,169,171,172,176,182,192,205,206,208,209,210,211,212,213,214,215,216,223,224,244,245,247,248,249,250,256,283,289,311,317,],[153,153,153,-119,153,153,-125,153,-149,153,-119,-119,153,-127,153,153,153,153,-119,-119,153,-119,-119,-119,-119,153,-127,153,153,153,153,153,153,153,153,153,-132,153,]),'CTESTRING':([120,192,223,224,256,],[158,-127,158,-127,158,]),'THEN':([194,225,323,326,],[-130,257,-131,328,]),'UNTIL':([196,],[227,]),'DO':([226,258,298,305,],[-136,282,-139,313,]),'ELIF':([296,331,],[302,302,]),'ELSE':([296,301,303,331,332,],[-110,309,-73,-110,-72,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'check_init':([4,],[5,]),'program_classes':([5,],[6,]),'classes':([5,13,],[7,17,]),'empty':([5,16,21,296,301,331,],[8,23,33,303,310,303,]),'add_class':([10,11,],[12,14,]),'classes_aux':([11,],[13,]),'program_body':([16,],[20,]),'program_body_vars':([16,],[21,]),'dec_vars':([16,18,47,73,164,],[22,25,58,84,199,]),'functions':([18,21,25,44,47,58,],[26,32,42,55,59,70,]),'add_inherit_class':([19,],[28,]),'init':([20,],[29,]),'program_body_funct':([21,],[31,]),'dec_vars_aux':([24,62,66,],[34,74,78,]),'dec_vars_simple':([24,62,66,],[35,35,35,]),'dec_vars_complex':([24,62,66,],[36,36,36,]),'simple_type':([24,27,62,66,80,81,201,202,],[37,46,37,37,105,105,105,105,]),'functions_aux':([27,],[44,]),'add_init':([30,],[49,]),'vars_simple_type':([37,75,76,],[50,99,100,]),'vars_complex_type':([38,79,],[52,102,]),'add_variable':([51,53,],[63,67,]),'vars_simple_type_aux':([51,],[64,]),'add_function':([56,57,],[68,69,]),'end_program':([60,],[72,]),'start_init':([61,],[73,]),'statutes_aux':([73,84,85,164,199,281,291,318,319,329,],[83,109,110,200,229,290,297,321,322,330,]),'statutes':([73,84,85,164,199,281,291,318,319,329,],[85,85,85,85,85,85,85,85,85,85,]),'assignation':([73,84,85,123,164,199,281,291,318,319,329,],[86,86,86,161,86,86,86,86,86,86,86,]),'read':([73,84,85,164,199,281,291,318,319,329,],[88,88,88,88,88,88,88,88,88,88,]),'write':([73,84,85,164,199,281,291,318,319,329,],[89,89,89,89,89,89,89,89,89,89,]),'condition':([73,84,85,164,199,281,291,318,319,329,],[90,90,90,90,90,90,90,90,90,90,]),'while':([73,84,85,164,199,281,291,318,319,329,],[91,91,91,91,91,91,91,91,91,91,]),'for':([73,84,85,164,199,281,291,318,319,329,],[92,92,92,92,92,92,92,92,92,92,]),'params':([80,81,201,202,],[103,107,232,233,]),'call':([87,118,120,121,160,171,182,205,206,208,209,212,223,244,245,247,248,249,250,256,283,289,317,],[112,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,147,]),'push_var':([93,115,149,151,152,153,155,179,185,],[114,137,184,186,187,188,190,184,219,]),'var_aux':([93,149,179,],[115,185,185,]),'var_aux_2':([93,138,149,179,218,],[117,173,117,117,173,]),'while_jump':([97,],[122,]),'add_array_variable':([101,],[125,]),'body':([104,106,163,168,],[127,130,198,204,]),'exist_function':([113,149,],[134,134,]),'exp':([118,120,121,160,171,182,205,206,208,209,223,244,245,256,283,289,317,],[139,157,159,195,207,217,238,238,242,243,157,271,272,157,292,238,320,]),'l_exp':([118,120,121,160,171,182,205,206,208,209,223,244,245,256,283,289,317,],[140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,140,]),'a_exp':([118,120,121,160,171,182,205,206,208,209,212,223,244,245,247,248,256,283,289,317,],[141,141,141,141,141,141,141,141,141,141,246,141,141,141,274,275,141,141,141,141,]),'term':([118,120,121,160,171,182,205,206,208,209,212,223,244,245,247,248,249,250,256,283,289,317,],[142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,142,276,277,142,142,142,142,]),'factor':([118,120,121,160,171,182,205,206,208,209,212,223,244,245,247,248,249,250,256,283,289,317,],[145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,145,]),'factor_aux':([118,120,121,160,171,182,205,206,208,209,212,223,244,245,247,248,249,250,256,283,289,317,],[148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,148,]),'cte':([118,120,121,143,144,160,171,182,205,206,208,209,212,223,244,245,247,248,249,250,256,283,289,317,],[150,150,150,178,180,150,150,150,150,150,150,150,150,150,150,150,150,150,150,150,150,150,150,150,]),'read_aux':([119,253,],[154,279,]),'write_aux':([120,223,256,],[156,255,280,]),'insert_number_params':([126,131,],[163,168,]),'start_function':([128,],[164,]),'add_param':([129,],[165,]),'params_aux':([129,],[166,]),'push_op':([136,172,176,210,211,213,214,215,216,],[171,208,212,244,245,247,248,249,250,]),'pop_op_lop':([140,],[175,]),'pop_op_art_n2':([142,],[177,]),'pop_op_art_n1':([145,],[181,]),'push_paren':([146,],[182,]),'save_string':([158,],[193,]),'era_function':([169,],[205,]),'generate_write':([192,222,224,],[223,254,256,]),'if_condition':([194,],[225,]),'add_matrix_variable':([197,],[228,]),'add_array_var_params':([203,],[235,]),'call_aux':([205,206,289,],[237,240,295,]),'pop_op_assign':([207,242,],[241,269,]),'generate_read':([220,221,],[252,253,]),'while_condition':([226,],[258,]),'for_jump':([227,],[259,]),'end_function':([230,260,300,306,],[262,284,307,314,]),'gosub_function':([236,266,],[265,288,]),'arg_function':([238,],[267,]),'pop_op_relop':([246,],[273,]),'pop_paren':([251,],[278,]),'return_function':([263,285,],[286,293,]),'add_matrix_var_params':([264,],[287,]),'condition_aux_elif':([296,331,],[301,332,]),'for_condition':([298,],[305,]),'condition_aux_else':([301,],[308,]),'end_while':([304,],[312,]),'end_if':([308,],[315,]),'else_condition':([309,],[316,]),'elif_expression':([311,],[317,]),'elif_condition':([323,],[326,]),'end_for':([324,],[327,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID TWOPOINTS check_init program_classes MAIN add_class LBRACE program_body init RBRACE END end_program','program',13,'p_program','parser.py',14),
  ('program_classes -> classes','program_classes',1,'p_program_classes','parser.py',18),
  ('program_classes -> empty','program_classes',1,'p_program_classes','parser.py',19),
  ('program_body -> program_body_vars program_body_funct','program_body',2,'p_program_body','parser.py',23),
  ('program_body_vars -> dec_vars','program_body_vars',1,'p_program_body_vars','parser.py',27),
  ('program_body_vars -> empty','program_body_vars',1,'p_program_body_vars','parser.py',28),
  ('program_body_funct -> functions','program_body_funct',1,'p_program_body_funct','parser.py',32),
  ('program_body_funct -> empty','program_body_funct',1,'p_program_body_funct','parser.py',33),
  ('dec_vars -> VAR dec_vars_aux','dec_vars',2,'p_dec_vars','parser.py',37),
  ('dec_vars_aux -> dec_vars_simple','dec_vars_aux',1,'p_dec_vars_aux','parser.py',41),
  ('dec_vars_aux -> dec_vars_complex','dec_vars_aux',1,'p_dec_vars_aux','parser.py',42),
  ('dec_vars_simple -> simple_type vars_simple_type SEMICOLON','dec_vars_simple',3,'p_dec_vars_simple','parser.py',46),
  ('dec_vars_simple -> simple_type vars_simple_type SEMICOLON dec_vars_aux','dec_vars_simple',4,'p_dec_vars_simple','parser.py',47),
  ('simple_type -> INT','simple_type',1,'p_simple_type','parser.py',51),
  ('simple_type -> FLOAT','simple_type',1,'p_simple_type','parser.py',52),
  ('simple_type -> CHAR','simple_type',1,'p_simple_type','parser.py',53),
  ('vars_simple_type -> ID add_variable','vars_simple_type',2,'p_vars_simple_type','parser.py',57),
  ('vars_simple_type -> ID add_variable COMMA vars_simple_type','vars_simple_type',4,'p_vars_simple_type','parser.py',58),
  ('vars_simple_type -> ID vars_simple_type_aux','vars_simple_type',2,'p_vars_simple_type','parser.py',59),
  ('vars_simple_type -> ID vars_simple_type_aux COMMA vars_simple_type','vars_simple_type',4,'p_vars_simple_type','parser.py',60),
  ('vars_simple_type_aux -> LBRACKET CTEI RBRACKET add_array_variable','vars_simple_type_aux',4,'p_vars_simple_type_aux','parser.py',64),
  ('vars_simple_type_aux -> LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET add_matrix_variable','vars_simple_type_aux',7,'p_vars_simple_type_aux','parser.py',65),
  ('dec_vars_complex -> OBJECT vars_complex_type SEMICOLON','dec_vars_complex',3,'p_dec_vars_complex','parser.py',69),
  ('dec_vars_complex -> OBJECT vars_complex_type SEMICOLON dec_vars_aux','dec_vars_complex',4,'p_dec_vars_complex','parser.py',70),
  ('vars_complex_type -> ID add_variable','vars_complex_type',2,'p_vars_complex_type','parser.py',74),
  ('vars_complex_type -> ID add_variable COMMA vars_complex_type','vars_complex_type',4,'p_vars_complex_type','parser.py',75),
  ('classes -> CLASS OBJECT classes_aux','classes',3,'p_classes','parser.py',79),
  ('classes -> CLASS OBJECT classes_aux classes','classes',4,'p_classes','parser.py',80),
  ('classes_aux -> add_class LBRACE dec_vars functions RBRACE','classes_aux',5,'p_classes_aux','parser.py',84),
  ('classes_aux -> add_class LBRACE functions RBRACE','classes_aux',4,'p_classes_aux','parser.py',85),
  ('classes_aux -> INHERITS OBJECT add_inherit_class LBRACE dec_vars functions RBRACE','classes_aux',7,'p_classes_aux','parser.py',86),
  ('classes_aux -> INHERITS OBJECT add_inherit_class LBRACE functions RBRACE','classes_aux',6,'p_classes_aux','parser.py',87),
  ('functions -> FUNCT functions_aux','functions',2,'p_functions','parser.py',91),
  ('functions -> FUNCT functions_aux functions','functions',3,'p_functions','parser.py',92),
  ('functions_aux -> VOID ID add_function LPAREN params RPAREN insert_number_params body','functions_aux',8,'p_functions_aux','parser.py',96),
  ('functions_aux -> VOID ID add_function LPAREN RPAREN body','functions_aux',6,'p_functions_aux','parser.py',97),
  ('functions_aux -> simple_type ID add_function LPAREN RPAREN body','functions_aux',6,'p_functions_aux','parser.py',98),
  ('functions_aux -> simple_type ID add_function LPAREN params RPAREN insert_number_params body','functions_aux',8,'p_functions_aux','parser.py',99),
  ('params -> simple_type ID add_param','params',3,'p_params','parser.py',103),
  ('params -> simple_type ID add_param COMMA params','params',5,'p_params','parser.py',104),
  ('params -> simple_type ID params_aux','params',3,'p_params','parser.py',105),
  ('params -> simple_type ID params_aux COMMA params','params',5,'p_params','parser.py',106),
  ('params_aux -> LBRACKET RBRACKET add_array_var_params','params_aux',3,'p_params_aux','parser.py',110),
  ('params_aux -> LBRACKET RBRACKET LBRACKET RBRACKET add_matrix_var_params','params_aux',5,'p_params_aux','parser.py',111),
  ('body -> LBRACE start_function dec_vars statutes_aux RBRACE end_function','body',6,'p_body','parser.py',114),
  ('body -> LBRACE start_function statutes_aux RBRACE end_function','body',5,'p_body','parser.py',115),
  ('body -> LBRACE start_function statutes_aux RETURN ID return_function SEMICOLON RBRACE end_function','body',9,'p_body','parser.py',116),
  ('body -> LBRACE start_function dec_vars statutes_aux RETURN ID return_function SEMICOLON RBRACE end_function','body',10,'p_body','parser.py',117),
  ('statutes -> assignation SEMICOLON','statutes',2,'p_statutes','parser.py',121),
  ('statutes -> CALL call SEMICOLON','statutes',3,'p_statutes','parser.py',122),
  ('statutes -> read','statutes',1,'p_statutes','parser.py',123),
  ('statutes -> write','statutes',1,'p_statutes','parser.py',124),
  ('statutes -> condition','statutes',1,'p_statutes','parser.py',125),
  ('statutes -> while','statutes',1,'p_statutes','parser.py',126),
  ('statutes -> for','statutes',1,'p_statutes','parser.py',127),
  ('statutes_aux -> statutes','statutes_aux',1,'p_statutes_aux','parser.py',131),
  ('statutes_aux -> statutes statutes_aux','statutes_aux',2,'p_statutes_aux','parser.py',132),
  ('assignation -> ID push_var EQUAL push_op exp pop_op_assign','assignation',6,'p_assignation','parser.py',136),
  ('assignation -> ID var_aux push_var EQUAL push_op exp pop_op_assign','assignation',7,'p_assignation','parser.py',137),
  ('var_aux -> POINT ID','var_aux',2,'p_var_aux','parser.py',141),
  ('var_aux -> POINT ID var_aux_2','var_aux',3,'p_var_aux','parser.py',142),
  ('var_aux -> var_aux_2','var_aux',1,'p_var_aux','parser.py',143),
  ('var_aux_2 -> LBRACKET exp RBRACKET','var_aux_2',3,'p_var_aux_2','parser.py',147),
  ('var_aux_2 -> LBRACKET exp RBRACKET LBRACKET exp RBRACKET','var_aux_2',6,'p_var_aux_2','parser.py',148),
  ('call -> ID exist_function LPAREN era_function RPAREN gosub_function','call',6,'p_call','parser.py',152),
  ('call -> ID POINT ID LPAREN RPAREN','call',5,'p_call','parser.py',153),
  ('call -> ID exist_function LPAREN era_function call_aux RPAREN gosub_function','call',7,'p_call','parser.py',154),
  ('call -> ID POINT ID LPAREN call_aux RPAREN','call',6,'p_call','parser.py',155),
  ('call_aux -> exp arg_function','call_aux',2,'p_call_aux','parser.py',159),
  ('call_aux -> exp arg_function COMMA call_aux','call_aux',4,'p_call_aux','parser.py',160),
  ('condition -> IF LPAREN exp RPAREN if_condition THEN LBRACE statutes_aux RBRACE condition_aux_elif condition_aux_else end_if','condition',12,'p_condition','parser.py',164),
  ('condition_aux_elif -> ELIF LPAREN elif_expression exp RPAREN elif_condition THEN LBRACE statutes_aux RBRACE condition_aux_elif','condition_aux_elif',11,'p_condition_aux_elif','parser.py',168),
  ('condition_aux_elif -> empty','condition_aux_elif',1,'p_condition_aux_elif','parser.py',169),
  ('condition_aux_else -> ELSE else_condition LBRACE statutes_aux RBRACE','condition_aux_else',5,'p_condition_aux_else','parser.py',173),
  ('condition_aux_else -> empty','condition_aux_else',1,'p_condition_aux_else','parser.py',174),
  ('read -> READ LPAREN read_aux RPAREN SEMICOLON generate_read','read',6,'p_read','parser.py',178),
  ('read_aux -> ID push_var','read_aux',2,'p_read_aux','parser.py',182),
  ('read_aux -> ID push_var COMMA generate_read read_aux','read_aux',5,'p_read_aux','parser.py',183),
  ('write -> WRITE LPAREN write_aux RPAREN SEMICOLON generate_write','write',6,'p_write','parser.py',187),
  ('write_aux -> exp','write_aux',1,'p_write_aux','parser.py',191),
  ('write_aux -> exp COMMA generate_write write_aux','write_aux',4,'p_write_aux','parser.py',192),
  ('write_aux -> CTESTRING save_string','write_aux',2,'p_write_aux','parser.py',193),
  ('write_aux -> CTESTRING save_string COMMA generate_write write_aux','write_aux',5,'p_write_aux','parser.py',194),
  ('while -> WHILE while_jump LPAREN exp RPAREN while_condition DO LBRACE statutes_aux RBRACE end_while','while',11,'p_while','parser.py',198),
  ('for -> FROM LPAREN assignation RPAREN UNTIL for_jump LPAREN exp RPAREN for_condition DO LBRACE statutes_aux RBRACE end_for','for',15,'p_for','parser.py',202),
  ('exp -> l_exp pop_op_lop','exp',2,'p_exp','parser.py',206),
  ('exp -> l_exp pop_op_lop OR push_op exp','exp',5,'p_exp','parser.py',207),
  ('exp -> l_exp pop_op_lop AND push_op exp','exp',5,'p_exp','parser.py',208),
  ('l_exp -> a_exp','l_exp',1,'p_l_exp','parser.py',212),
  ('l_exp -> a_exp RELOP push_op a_exp pop_op_relop','l_exp',5,'p_l_exp','parser.py',213),
  ('a_exp -> term pop_op_art_n2','a_exp',2,'p_a_exp','parser.py',217),
  ('a_exp -> term pop_op_art_n2 PLUS push_op a_exp','a_exp',5,'p_a_exp','parser.py',218),
  ('a_exp -> term pop_op_art_n2 MINUS push_op a_exp','a_exp',5,'p_a_exp','parser.py',219),
  ('term -> factor pop_op_art_n1','term',2,'p_term','parser.py',223),
  ('term -> factor pop_op_art_n1 TIMES push_op term','term',5,'p_term','parser.py',224),
  ('term -> factor pop_op_art_n1 DIVIDE push_op term','term',5,'p_term','parser.py',225),
  ('factor -> LPAREN push_paren exp RPAREN pop_paren','factor',5,'p_factor','parser.py',229),
  ('factor -> call','factor',1,'p_factor','parser.py',230),
  ('factor -> factor_aux','factor',1,'p_factor','parser.py',231),
  ('factor_aux -> cte','factor_aux',1,'p_factor_aux','parser.py',235),
  ('factor_aux -> PLUS cte','factor_aux',2,'p_factor_aux','parser.py',236),
  ('factor_aux -> MINUS cte','factor_aux',2,'p_factor_aux','parser.py',237),
  ('cte -> ID push_var','cte',2,'p_cte','parser.py',241),
  ('cte -> ID var_aux push_var','cte',3,'p_cte','parser.py',242),
  ('cte -> CTEI push_var','cte',2,'p_cte','parser.py',243),
  ('cte -> CTEF push_var','cte',2,'p_cte','parser.py',244),
  ('cte -> CTECHAR push_var','cte',2,'p_cte','parser.py',245),
  ('init -> INIT add_init LBRACE start_init statutes_aux RBRACE','init',6,'p_init','parser.py',249),
  ('init -> INIT add_init LBRACE start_init dec_vars statutes_aux RBRACE','init',7,'p_init','parser.py',250),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',254),
  ('add_variable -> <empty>','add_variable',0,'p_add_variable','parser.py',263),
  ('add_array_variable -> <empty>','add_array_variable',0,'p_add_array_variable','parser.py',268),
  ('add_matrix_variable -> <empty>','add_matrix_variable',0,'p_add_matrix_variable','parser.py',273),
  ('add_function -> <empty>','add_function',0,'p_add_function','parser.py',278),
  ('add_init -> <empty>','add_init',0,'p_add_init','parser.py',282),
  ('add_class -> <empty>','add_class',0,'p_add_class','parser.py',286),
  ('add_inherit_class -> <empty>','add_inherit_class',0,'p_add_inherit_class','parser.py',290),
  ('push_var -> <empty>','push_var',0,'p_push_var','parser.py',296),
  ('push_op -> <empty>','push_op',0,'p_push_op','parser.py',300),
  ('pop_op_art_n1 -> <empty>','pop_op_art_n1',0,'p_pop_op_art_n1','parser.py',304),
  ('pop_op_art_n2 -> <empty>','pop_op_art_n2',0,'p_pop_op_art_n2','parser.py',308),
  ('pop_op_relop -> <empty>','pop_op_relop',0,'p_pop_op_relop','parser.py',312),
  ('pop_op_lop -> <empty>','pop_op_lop',0,'p_pop_op_lop','parser.py',316),
  ('pop_op_assign -> <empty>','pop_op_assign',0,'p_pop_op_assign','parser.py',320),
  ('push_paren -> <empty>','push_paren',0,'p_push_paren','parser.py',324),
  ('pop_paren -> <empty>','pop_paren',0,'p_pop_paren','parser.py',328),
  ('generate_write -> <empty>','generate_write',0,'p_generate_write','parser.py',334),
  ('save_string -> <empty>','save_string',0,'p_save_string','parser.py',338),
  ('generate_read -> <empty>','generate_read',0,'p_generate_read','parser.py',342),
  ('if_condition -> <empty>','if_condition',0,'p_if_condition','parser.py',348),
  ('elif_condition -> <empty>','elif_condition',0,'p_elif_condition','parser.py',352),
  ('elif_expression -> <empty>','elif_expression',0,'p_elif_expression','parser.py',356),
  ('else_condition -> <empty>','else_condition',0,'p_else_condition','parser.py',360),
  ('end_if -> <empty>','end_if',0,'p_end_if','parser.py',364),
  ('while_jump -> <empty>','while_jump',0,'p_while_jump','parser.py',368),
  ('while_condition -> <empty>','while_condition',0,'p_while_condition','parser.py',372),
  ('end_while -> <empty>','end_while',0,'p_end_while','parser.py',376),
  ('for_jump -> <empty>','for_jump',0,'p_for_jump','parser.py',380),
  ('for_condition -> <empty>','for_condition',0,'p_for_condition','parser.py',384),
  ('end_for -> <empty>','end_for',0,'p_end_for','parser.py',388),
  ('add_param -> <empty>','add_param',0,'p_add_param','parser.py',394),
  ('add_array_var_params -> <empty>','add_array_var_params',0,'p_add_array_var_params','parser.py',398),
  ('add_matrix_var_params -> <empty>','add_matrix_var_params',0,'p_add_matrix_var_params','parser.py',403),
  ('insert_number_params -> <empty>','insert_number_params',0,'p_insert_number_params','parser.py',408),
  ('start_function -> <empty>','start_function',0,'p_start_function','parser.py',412),
  ('return_function -> <empty>','return_function',0,'p_return_function','parser.py',416),
  ('end_function -> <empty>','end_function',0,'p_end_function','parser.py',420),
  ('exist_function -> <empty>','exist_function',0,'p_exist_function','parser.py',424),
  ('era_function -> <empty>','era_function',0,'p_era_function','parser.py',428),
  ('arg_function -> <empty>','arg_function',0,'p_arg_function','parser.py',432),
  ('gosub_function -> <empty>','gosub_function',0,'p_gosub_function','parser.py',436),
  ('check_init -> <empty>','check_init',0,'p_check_init','parser.py',442),
  ('start_init -> <empty>','start_init',0,'p_start_init','parser.py',446),
  ('end_program -> <empty>','end_program',0,'p_end_program','parser.py',452),
]

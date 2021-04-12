
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASSIGN BOOL CALL CHAR CLASS COMMA CTECHAR CTEF CTEI CTESTRING DIVIDE DO ELIF ELSE END EQUAL FALSE FLOAT FROM FUNCT ID IF INHERITS INT LBRACE LBRACKET LPAREN MAIN MINUS OR PLUS POINT PROGRAM RBRACE RBRACKET READ RELOP RETURN RPAREN SEMICOLON THEN TIMES TRUE TWOPOINTS UNTIL VAR VOID WHILE WRITEprogram : PROGRAM ID TWOPOINTS program_body main ENDprogram_body : program_body_vars program_body_class program_body_functprogram_body_vars : dec_vars \n                        | emptyprogram_body_class : classes \n                        | emptyprogram_body_funct : functions \n                        | emptydec_vars : VAR dec_vars_auxdec_vars_aux : simple_type vars_simple_type SEMICOLON\n                    | simple_type vars_simple_type SEMICOLON dec_vars_aux\n                    | complex_type vars_complex_type SEMICOLON\n                    | complex_type vars_complex_type SEMICOLON dec_vars_auxvars_complex_type : ID \n                        | ID COMMA vars_complex_typevars_simple_type : ID \n                        | ID COMMA vars_simple_type\n                        | ID vars_simple_type_aux\n                        | ID vars_simple_type_aux COMMA vars_simple_typevars_simple_type_aux : LBRACKET CTEI RBRACKET\n                            | LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKETsimple_type : INT \n                    | FLOAT \n                    | CHAR \n                    | BOOLcomplex_type : IDclasses : CLASS ID classes_aux \n                | CLASS ID classes_aux classesclasses_aux : LBRACE dec_vars functions RBRACE\n                    | LBRACE functions RBRACE\n                    | INHERITS ID LBRACE dec_vars functions RBRACE\n                    | INHERITS ID LBRACE functions RBRACEfunctions : FUNCT functions_aux\n                | FUNCT functions_aux functionsfunctions_aux : VOID ID LPAREN params RPAREN body\n                    | VOID ID LPAREN RPAREN body\n                    | simple_type ID LPAREN RPAREN body\n                    | simple_type ID LPAREN params RPAREN bodyparams : simple_type ID\n            | simple_type ID COMMA paramsbody : LBRACE dec_vars statutes_aux RBRACE\n            | LBRACE statutes_aux RBRACE\n            | LBRACE statutes_aux RETURN ID RBRACE\n            | LBRACE dec_vars statutes_aux RETURN ID RBRACEstatutes : ASSIGN assignation\n                | CALL call SEMICOLON\n                | read\n                | write\n                | condition\n                | while\n                | forstatutes_aux : statutes\n                    | statutes statutes_auxassignation : var EQUAL exp SEMICOLONvar : ID\n            | ID var_auxvar_aux : POINT ID \n            |  POINT ID var_aux_2\n            |  var_aux_2var_aux_2 : LBRACKET exp RBRACKET\n            |  LBRACKET exp RBRACKET LBRACKET exp RBRACKETcall : ID LPAREN RPAREN\n            | ID POINT ID LPAREN RPAREN\n            | ID LPAREN call_aux RPAREN\n            | ID POINT ID LPAREN call_aux RPARENcall_aux : exp\n                | exp COMMA call_auxcondition : IF condition_auxcondition_aux : LPAREN exp RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_3\n                    | condition_aux_2condition_aux_2 : LPAREN exp RPAREN THEN LBRACE statutes_aux RBRACE ELIF condition_auxcondition_aux_3 : ELSE LBRACE statutes_aux RBRACE\n                        | emptyread : READ LPAREN var RPAREN SEMICOLONwrite : WRITE LPAREN write_aux RPAREN SEMICOLONwrite_aux : exp\n                | exp COMMA write_aux\n                | CTESTRING\n                | CTESTRING COMMA write_auxwhile : WHILE LPAREN exp RPAREN DO LBRACE statutes_aux RBRACEfor : FROM LPAREN exp RPAREN UNTIL LPAREN exp RPAREN DO LBRACE statutes_aux RBRACEexp : n_exp\n            | n_exp OR expn_exp : l_exp\n            | l_exp AND n_expl_exp : a_exp\n            | a_exp RELOP a_expa_exp : term\n            | term PLUS a_exp\n            | term MINUS a_expterm : factor\n            | factor TIMES term\n            | factor DIVIDE termfactor : LPAREN exp RPAREN\n            | var\n            | call\n            | factor_auxfactor_aux : cte\n                | PLUS cte\n                | MINUS ctecte : ID\n        | CTEI\n        | CTEF\n        | CTECHAR\n        | boolbool : TRUE\n        | FALSEmain : MAIN LBRACE statutes_aux RBRACE\n            | MAIN LBRACE dec_vars statutes_aux RBRACEempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,24,],[0,-1,]),'ID':([2,9,15,17,18,19,20,21,22,23,38,39,51,52,55,56,57,60,61,70,71,73,75,76,86,91,93,95,97,98,100,108,109,142,143,144,145,146,147,148,152,153,154,160,171,172,198,204,219,226,],[3,23,30,32,34,-22,-23,-24,-25,-26,67,69,78,79,83,23,32,23,34,67,114,114,114,114,32,114,133,114,114,138,114,150,150,114,114,114,114,114,114,114,114,114,185,192,114,114,114,114,227,233,]),'TWOPOINTS':([3,],[4,]),'VAR':([4,25,54,129,191,],[9,9,9,9,9,]),'CLASS':([4,6,7,8,16,53,56,60,84,88,128,163,196,210,],[-110,15,-3,-4,-9,15,-10,-12,-11,-13,-30,-29,-32,-31,]),'FUNCT':([4,6,7,8,12,13,14,16,50,53,54,56,60,80,81,84,88,128,129,163,164,190,193,196,205,209,210,218,225,234,238,],[-110,-110,-3,-4,29,-5,-6,-9,29,-27,29,-10,-12,-28,29,-11,-13,-30,29,-29,29,-36,-37,-32,-35,-38,-31,-42,-41,-43,-44,]),'MAIN':([4,5,6,7,8,12,13,14,16,26,27,28,50,53,56,60,77,80,84,88,128,163,190,193,196,205,209,210,218,225,234,238,],[-110,11,-110,-3,-4,-110,-5,-6,-9,-2,-7,-8,-33,-27,-10,-12,-34,-28,-11,-13,-30,-29,-36,-37,-32,-35,-38,-31,-42,-41,-43,-44,]),'INT':([9,29,56,60,125,126,208,],[19,19,19,19,19,19,19,]),'FLOAT':([9,29,56,60,125,126,208,],[20,20,20,20,20,20,20,]),'CHAR':([9,29,56,60,125,126,208,],[21,21,21,21,21,21,21,]),'BOOL':([9,29,56,60,125,126,208,],[22,22,22,22,22,22,22,]),'END':([10,62,90,],[24,-108,-109,]),'LBRACE':([11,30,83,159,161,186,187,189,194,230,232,],[25,54,129,191,191,202,203,191,191,236,237,]),'ASSIGN':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,38,38,38,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,38,38,38,38,-110,-80,-69,-73,-71,38,38,-72,-81,]),'CALL':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,39,39,39,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,39,39,39,39,-110,-80,-69,-73,-71,39,39,-72,-81,]),'READ':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,45,45,45,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,45,45,45,45,-110,-80,-69,-73,-71,45,45,-72,-81,]),'WRITE':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,46,46,46,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,46,46,46,46,-110,-80,-69,-73,-71,46,46,-72,-81,]),'IF':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,47,47,47,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,47,47,47,47,-110,-80,-69,-73,-71,47,47,-72,-81,]),'WHILE':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,48,48,48,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,48,48,48,48,-110,-80,-69,-73,-71,48,48,-72,-81,]),'FROM':([16,25,36,37,40,41,42,43,44,56,60,65,72,74,84,88,96,167,173,175,191,202,203,206,222,223,228,231,235,236,237,241,242,],[-9,49,49,49,-47,-48,-49,-50,-51,-10,-12,-45,-68,-70,-11,-13,-46,-54,-74,-75,49,49,49,49,-110,-80,-69,-73,-71,49,49,-72,-81,]),'VOID':([29,],[51,]),'INHERITS':([30,],[55,]),'SEMICOLON':([31,32,33,34,58,68,85,89,92,94,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,130,131,132,135,139,141,149,150,151,168,169,170,174,178,179,180,181,182,183,184,185,200,211,213,221,],[56,-16,60,-14,-18,96,-17,-15,-56,-59,-82,-84,-86,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-19,-20,167,-62,173,175,-99,-101,-100,-58,-60,-64,-94,-83,-85,-87,-89,-90,-92,-93,-57,-63,-21,-65,-61,]),'COMMA':([32,34,58,92,94,102,103,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,131,135,137,149,150,151,168,169,170,174,178,179,180,181,182,183,184,185,192,200,211,213,221,],[57,61,86,-56,-59,142,143,-82,-84,-86,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-20,-62,171,-99,-101,-100,-58,-60,-64,-94,-83,-85,-87,-89,-90,-92,-93,-57,208,-63,-21,-65,-61,]),'LBRACKET':([32,67,114,131,133,169,185,],[59,95,95,166,95,198,95,]),'RBRACE':([35,37,40,41,42,43,44,50,63,64,65,72,74,77,82,96,127,165,167,173,175,190,193,195,205,207,209,214,215,217,218,222,223,225,227,228,231,233,234,235,238,239,240,241,242,],[62,-52,-47,-48,-49,-50,-51,-33,90,-53,-45,-68,-70,-34,128,-46,163,196,-54,-74,-75,-36,-37,210,-35,218,-38,222,223,225,-42,-110,-80,-41,234,-69,-73,238,-43,-71,-44,241,242,-72,-81,]),'RETURN':([37,40,41,42,43,44,64,65,72,74,96,167,173,175,207,217,222,223,228,231,235,241,242,],[-52,-47,-48,-49,-50,-51,-53,-45,-68,-70,-46,-54,-74,-75,219,226,-110,-80,-69,-73,-71,-72,-81,]),'LPAREN':([45,46,47,48,49,69,71,73,75,76,78,79,91,95,97,100,114,138,142,143,144,145,146,147,148,152,153,171,172,185,188,198,204,229,],[70,71,73,75,76,97,100,100,100,100,125,126,100,100,100,100,97,172,100,100,100,100,100,100,100,100,100,100,100,172,204,100,100,73,]),'CTEI':([59,71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,166,171,172,198,204,],[87,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,116,197,116,116,116,116,]),'EQUAL':([66,67,92,94,133,168,169,221,],[91,-55,-56,-59,-57,-58,-60,-61,]),'RPAREN':([67,92,94,97,99,101,102,103,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,133,135,136,137,140,149,150,151,158,162,168,169,170,172,174,176,177,178,179,180,181,182,183,184,185,192,199,200,201,213,216,220,221,],[-55,-56,-59,135,139,141,-76,-78,-82,-84,-86,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,155,156,157,159,161,-57,-62,170,-66,174,-99,-101,-100,189,194,-58,-60,-64,200,-94,-77,-79,-83,-85,-87,-89,-90,-92,-93,-57,-39,-67,-63,213,-65,224,-40,-61,]),'POINT':([67,69,114,],[93,98,154,]),'CTESTRING':([71,142,143,],[103,103,103,]),'PLUS':([71,73,75,76,91,92,94,95,97,100,107,110,111,112,113,114,115,116,117,118,119,120,121,135,142,143,144,145,146,147,148,149,150,151,152,153,168,169,170,171,172,174,183,184,185,198,200,204,213,221,],[108,108,108,108,108,-56,-59,108,108,108,147,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,108,108,108,108,108,108,108,-99,-101,-100,108,108,-58,-60,-64,108,108,-94,-92,-93,-57,108,-63,108,-65,-61,]),'MINUS':([71,73,75,76,91,92,94,95,97,100,107,110,111,112,113,114,115,116,117,118,119,120,121,135,142,143,144,145,146,147,148,149,150,151,152,153,168,169,170,171,172,174,183,184,185,198,200,204,213,221,],[109,109,109,109,109,-56,-59,109,109,109,148,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,109,109,109,109,109,109,109,-99,-101,-100,109,109,-58,-60,-64,109,109,-94,-92,-93,-57,109,-63,109,-65,-61,]),'CTEF':([71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,171,172,198,204,],[117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,117,]),'CTECHAR':([71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,171,172,198,204,],[118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,118,]),'TRUE':([71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,171,172,198,204,],[120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,120,]),'FALSE':([71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,171,172,198,204,],[121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,121,]),'RBRACKET':([87,92,94,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,134,135,149,150,151,168,169,170,174,178,179,180,181,182,183,184,185,197,200,212,213,221,],[131,-56,-59,-82,-84,-86,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,169,-62,-99,-101,-100,-58,-60,-64,-94,-83,-85,-87,-89,-90,-92,-93,-57,211,-63,221,-65,-61,]),'TIMES':([92,94,110,111,112,113,114,115,116,117,118,119,120,121,135,149,150,151,168,169,170,174,185,200,213,221,],[-56,-59,152,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,-99,-101,-100,-58,-60,-64,-94,-57,-63,-65,-61,]),'DIVIDE':([92,94,110,111,112,113,114,115,116,117,118,119,120,121,135,149,150,151,168,169,170,174,185,200,213,221,],[-56,-59,153,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,-99,-101,-100,-58,-60,-64,-94,-57,-63,-65,-61,]),'RELOP':([92,94,106,107,110,111,112,113,114,115,116,117,118,119,120,121,135,149,150,151,168,169,170,174,181,182,183,184,185,200,213,221,],[-56,-59,146,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,-99,-101,-100,-58,-60,-64,-94,-89,-90,-92,-93,-57,-63,-65,-61,]),'AND':([92,94,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,135,149,150,151,168,169,170,174,180,181,182,183,184,185,200,213,221,],[-56,-59,145,-86,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,-99,-101,-100,-58,-60,-64,-94,-87,-89,-90,-92,-93,-57,-63,-65,-61,]),'OR':([92,94,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,135,149,150,151,168,169,170,174,179,180,181,182,183,184,185,200,213,221,],[-56,-59,144,-84,-86,-88,-91,-95,-96,-97,-55,-98,-102,-103,-104,-105,-106,-107,-62,-99,-101,-100,-58,-60,-64,-94,-85,-87,-89,-90,-92,-93,-57,-63,-65,-61,]),'THEN':([155,],[186,]),'DO':([156,224,],[187,232,]),'UNTIL':([157,],[188,]),'ELIF':([222,],[229,]),'ELSE':([222,],[230,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'program_body':([4,],[5,]),'program_body_vars':([4,],[6,]),'dec_vars':([4,25,54,129,191,],[7,36,81,164,206,]),'empty':([4,6,12,222,],[8,14,28,231,]),'main':([5,],[10,]),'program_body_class':([6,],[12,]),'classes':([6,53,],[13,80,]),'dec_vars_aux':([9,56,60,],[16,84,88,]),'simple_type':([9,29,56,60,125,126,208,],[17,52,17,17,160,160,160,]),'complex_type':([9,56,60,],[18,18,18,]),'program_body_funct':([12,],[26,]),'functions':([12,50,54,81,129,164,],[27,77,82,127,165,195,]),'vars_simple_type':([17,57,86,],[31,85,130,]),'vars_complex_type':([18,61,],[33,89,]),'statutes_aux':([25,36,37,191,202,203,206,236,237,],[35,63,64,207,214,215,217,239,240,]),'statutes':([25,36,37,191,202,203,206,236,237,],[37,37,37,37,37,37,37,37,37,]),'read':([25,36,37,191,202,203,206,236,237,],[40,40,40,40,40,40,40,40,40,]),'write':([25,36,37,191,202,203,206,236,237,],[41,41,41,41,41,41,41,41,41,]),'condition':([25,36,37,191,202,203,206,236,237,],[42,42,42,42,42,42,42,42,42,]),'while':([25,36,37,191,202,203,206,236,237,],[43,43,43,43,43,43,43,43,43,]),'for':([25,36,37,191,202,203,206,236,237,],[44,44,44,44,44,44,44,44,44,]),'functions_aux':([29,],[50,]),'classes_aux':([30,],[53,]),'vars_simple_type_aux':([32,],[58,]),'assignation':([38,],[65,]),'var':([38,70,71,73,75,76,91,95,97,100,142,143,144,145,146,147,148,152,153,171,172,198,204,],[66,99,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,111,]),'call':([39,71,73,75,76,91,95,97,100,142,143,144,145,146,147,148,152,153,171,172,198,204,],[68,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,112,]),'condition_aux':([47,229,],[72,235,]),'condition_aux_2':([47,229,],[74,74,]),'var_aux':([67,114,],[92,92,]),'var_aux_2':([67,114,133,185,],[94,94,168,168,]),'write_aux':([71,142,143,],[101,176,177,]),'exp':([71,73,75,76,91,95,97,100,142,143,144,171,172,198,204,],[102,122,123,124,132,134,137,140,102,102,178,137,137,212,216,]),'n_exp':([71,73,75,76,91,95,97,100,142,143,144,145,171,172,198,204,],[104,104,104,104,104,104,104,104,104,104,104,179,104,104,104,104,]),'l_exp':([71,73,75,76,91,95,97,100,142,143,144,145,171,172,198,204,],[105,105,105,105,105,105,105,105,105,105,105,105,105,105,105,105,]),'a_exp':([71,73,75,76,91,95,97,100,142,143,144,145,146,147,148,171,172,198,204,],[106,106,106,106,106,106,106,106,106,106,106,106,180,181,182,106,106,106,106,]),'term':([71,73,75,76,91,95,97,100,142,143,144,145,146,147,148,152,153,171,172,198,204,],[107,107,107,107,107,107,107,107,107,107,107,107,107,107,107,183,184,107,107,107,107,]),'factor':([71,73,75,76,91,95,97,100,142,143,144,145,146,147,148,152,153,171,172,198,204,],[110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,110,]),'factor_aux':([71,73,75,76,91,95,97,100,142,143,144,145,146,147,148,152,153,171,172,198,204,],[113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,113,]),'cte':([71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,171,172,198,204,],[115,115,115,115,115,115,115,115,149,151,115,115,115,115,115,115,115,115,115,115,115,115,115,]),'bool':([71,73,75,76,91,95,97,100,108,109,142,143,144,145,146,147,148,152,153,171,172,198,204,],[119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,119,]),'call_aux':([97,171,172,],[136,199,201,]),'params':([125,126,208,],[158,162,220,]),'body':([159,161,189,194,],[190,193,205,209,]),'condition_aux_3':([222,],[228,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID TWOPOINTS program_body main END','program',6,'p_program','parser.py',5),
  ('program_body -> program_body_vars program_body_class program_body_funct','program_body',3,'p_program_body','parser.py',9),
  ('program_body_vars -> dec_vars','program_body_vars',1,'p_program_body_vars','parser.py',13),
  ('program_body_vars -> empty','program_body_vars',1,'p_program_body_vars','parser.py',14),
  ('program_body_class -> classes','program_body_class',1,'p_program_body_class','parser.py',18),
  ('program_body_class -> empty','program_body_class',1,'p_program_body_class','parser.py',19),
  ('program_body_funct -> functions','program_body_funct',1,'p_program_body_funct','parser.py',23),
  ('program_body_funct -> empty','program_body_funct',1,'p_program_body_funct','parser.py',24),
  ('dec_vars -> VAR dec_vars_aux','dec_vars',2,'p_dec_vars','parser.py',28),
  ('dec_vars_aux -> simple_type vars_simple_type SEMICOLON','dec_vars_aux',3,'p_dec_vars_aux','parser.py',32),
  ('dec_vars_aux -> simple_type vars_simple_type SEMICOLON dec_vars_aux','dec_vars_aux',4,'p_dec_vars_aux','parser.py',33),
  ('dec_vars_aux -> complex_type vars_complex_type SEMICOLON','dec_vars_aux',3,'p_dec_vars_aux','parser.py',34),
  ('dec_vars_aux -> complex_type vars_complex_type SEMICOLON dec_vars_aux','dec_vars_aux',4,'p_dec_vars_aux','parser.py',35),
  ('vars_complex_type -> ID','vars_complex_type',1,'p_vars_complex_type','parser.py',39),
  ('vars_complex_type -> ID COMMA vars_complex_type','vars_complex_type',3,'p_vars_complex_type','parser.py',40),
  ('vars_simple_type -> ID','vars_simple_type',1,'p_vars_simple_type','parser.py',44),
  ('vars_simple_type -> ID COMMA vars_simple_type','vars_simple_type',3,'p_vars_simple_type','parser.py',45),
  ('vars_simple_type -> ID vars_simple_type_aux','vars_simple_type',2,'p_vars_simple_type','parser.py',46),
  ('vars_simple_type -> ID vars_simple_type_aux COMMA vars_simple_type','vars_simple_type',4,'p_vars_simple_type','parser.py',47),
  ('vars_simple_type_aux -> LBRACKET CTEI RBRACKET','vars_simple_type_aux',3,'p_vars_simple_type_aux','parser.py',51),
  ('vars_simple_type_aux -> LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET','vars_simple_type_aux',6,'p_vars_simple_type_aux','parser.py',52),
  ('simple_type -> INT','simple_type',1,'p_simple_type','parser.py',56),
  ('simple_type -> FLOAT','simple_type',1,'p_simple_type','parser.py',57),
  ('simple_type -> CHAR','simple_type',1,'p_simple_type','parser.py',58),
  ('simple_type -> BOOL','simple_type',1,'p_simple_type','parser.py',59),
  ('complex_type -> ID','complex_type',1,'p_complex_type','parser.py',63),
  ('classes -> CLASS ID classes_aux','classes',3,'p_classes','parser.py',67),
  ('classes -> CLASS ID classes_aux classes','classes',4,'p_classes','parser.py',68),
  ('classes_aux -> LBRACE dec_vars functions RBRACE','classes_aux',4,'p_classes_aux','parser.py',72),
  ('classes_aux -> LBRACE functions RBRACE','classes_aux',3,'p_classes_aux','parser.py',73),
  ('classes_aux -> INHERITS ID LBRACE dec_vars functions RBRACE','classes_aux',6,'p_classes_aux','parser.py',74),
  ('classes_aux -> INHERITS ID LBRACE functions RBRACE','classes_aux',5,'p_classes_aux','parser.py',75),
  ('functions -> FUNCT functions_aux','functions',2,'p_functions','parser.py',79),
  ('functions -> FUNCT functions_aux functions','functions',3,'p_functions','parser.py',80),
  ('functions_aux -> VOID ID LPAREN params RPAREN body','functions_aux',6,'p_functions_aux','parser.py',84),
  ('functions_aux -> VOID ID LPAREN RPAREN body','functions_aux',5,'p_functions_aux','parser.py',85),
  ('functions_aux -> simple_type ID LPAREN RPAREN body','functions_aux',5,'p_functions_aux','parser.py',86),
  ('functions_aux -> simple_type ID LPAREN params RPAREN body','functions_aux',6,'p_functions_aux','parser.py',87),
  ('params -> simple_type ID','params',2,'p_params','parser.py',91),
  ('params -> simple_type ID COMMA params','params',4,'p_params','parser.py',92),
  ('body -> LBRACE dec_vars statutes_aux RBRACE','body',4,'p_body','parser.py',96),
  ('body -> LBRACE statutes_aux RBRACE','body',3,'p_body','parser.py',97),
  ('body -> LBRACE statutes_aux RETURN ID RBRACE','body',5,'p_body','parser.py',98),
  ('body -> LBRACE dec_vars statutes_aux RETURN ID RBRACE','body',6,'p_body','parser.py',99),
  ('statutes -> ASSIGN assignation','statutes',2,'p_statutes','parser.py',103),
  ('statutes -> CALL call SEMICOLON','statutes',3,'p_statutes','parser.py',104),
  ('statutes -> read','statutes',1,'p_statutes','parser.py',105),
  ('statutes -> write','statutes',1,'p_statutes','parser.py',106),
  ('statutes -> condition','statutes',1,'p_statutes','parser.py',107),
  ('statutes -> while','statutes',1,'p_statutes','parser.py',108),
  ('statutes -> for','statutes',1,'p_statutes','parser.py',109),
  ('statutes_aux -> statutes','statutes_aux',1,'p_statutes_aux','parser.py',113),
  ('statutes_aux -> statutes statutes_aux','statutes_aux',2,'p_statutes_aux','parser.py',114),
  ('assignation -> var EQUAL exp SEMICOLON','assignation',4,'p_assignation','parser.py',118),
  ('var -> ID','var',1,'p_var','parser.py',122),
  ('var -> ID var_aux','var',2,'p_var','parser.py',123),
  ('var_aux -> POINT ID','var_aux',2,'p_var_aux','parser.py',127),
  ('var_aux -> POINT ID var_aux_2','var_aux',3,'p_var_aux','parser.py',128),
  ('var_aux -> var_aux_2','var_aux',1,'p_var_aux','parser.py',129),
  ('var_aux_2 -> LBRACKET exp RBRACKET','var_aux_2',3,'p_var_aux_2','parser.py',133),
  ('var_aux_2 -> LBRACKET exp RBRACKET LBRACKET exp RBRACKET','var_aux_2',6,'p_var_aux_2','parser.py',134),
  ('call -> ID LPAREN RPAREN','call',3,'p_call','parser.py',138),
  ('call -> ID POINT ID LPAREN RPAREN','call',5,'p_call','parser.py',139),
  ('call -> ID LPAREN call_aux RPAREN','call',4,'p_call','parser.py',140),
  ('call -> ID POINT ID LPAREN call_aux RPAREN','call',6,'p_call','parser.py',141),
  ('call_aux -> exp','call_aux',1,'p_call_aux','parser.py',145),
  ('call_aux -> exp COMMA call_aux','call_aux',3,'p_call_aux','parser.py',146),
  ('condition -> IF condition_aux','condition',2,'p_condition','parser.py',150),
  ('condition_aux -> LPAREN exp RPAREN THEN LBRACE statutes_aux RBRACE condition_aux_3','condition_aux',8,'p_condition_aux','parser.py',154),
  ('condition_aux -> condition_aux_2','condition_aux',1,'p_condition_aux','parser.py',155),
  ('condition_aux_2 -> LPAREN exp RPAREN THEN LBRACE statutes_aux RBRACE ELIF condition_aux','condition_aux_2',9,'p_condition_aux_2','parser.py',159),
  ('condition_aux_3 -> ELSE LBRACE statutes_aux RBRACE','condition_aux_3',4,'p_condition_aux_3','parser.py',163),
  ('condition_aux_3 -> empty','condition_aux_3',1,'p_condition_aux_3','parser.py',164),
  ('read -> READ LPAREN var RPAREN SEMICOLON','read',5,'p_read','parser.py',168),
  ('write -> WRITE LPAREN write_aux RPAREN SEMICOLON','write',5,'p_write','parser.py',172),
  ('write_aux -> exp','write_aux',1,'p_write_aux','parser.py',176),
  ('write_aux -> exp COMMA write_aux','write_aux',3,'p_write_aux','parser.py',177),
  ('write_aux -> CTESTRING','write_aux',1,'p_write_aux','parser.py',178),
  ('write_aux -> CTESTRING COMMA write_aux','write_aux',3,'p_write_aux','parser.py',179),
  ('while -> WHILE LPAREN exp RPAREN DO LBRACE statutes_aux RBRACE','while',8,'p_while','parser.py',183),
  ('for -> FROM LPAREN exp RPAREN UNTIL LPAREN exp RPAREN DO LBRACE statutes_aux RBRACE','for',12,'p_for','parser.py',187),
  ('exp -> n_exp','exp',1,'p_exp','parser.py',191),
  ('exp -> n_exp OR exp','exp',3,'p_exp','parser.py',192),
  ('n_exp -> l_exp','n_exp',1,'p_n_exp','parser.py',196),
  ('n_exp -> l_exp AND n_exp','n_exp',3,'p_n_exp','parser.py',197),
  ('l_exp -> a_exp','l_exp',1,'p_l_exp','parser.py',201),
  ('l_exp -> a_exp RELOP a_exp','l_exp',3,'p_l_exp','parser.py',202),
  ('a_exp -> term','a_exp',1,'p_a_exp','parser.py',206),
  ('a_exp -> term PLUS a_exp','a_exp',3,'p_a_exp','parser.py',207),
  ('a_exp -> term MINUS a_exp','a_exp',3,'p_a_exp','parser.py',208),
  ('term -> factor','term',1,'p_term','parser.py',212),
  ('term -> factor TIMES term','term',3,'p_term','parser.py',213),
  ('term -> factor DIVIDE term','term',3,'p_term','parser.py',214),
  ('factor -> LPAREN exp RPAREN','factor',3,'p_factor','parser.py',218),
  ('factor -> var','factor',1,'p_factor','parser.py',219),
  ('factor -> call','factor',1,'p_factor','parser.py',220),
  ('factor -> factor_aux','factor',1,'p_factor','parser.py',221),
  ('factor_aux -> cte','factor_aux',1,'p_factor_aux','parser.py',225),
  ('factor_aux -> PLUS cte','factor_aux',2,'p_factor_aux','parser.py',226),
  ('factor_aux -> MINUS cte','factor_aux',2,'p_factor_aux','parser.py',227),
  ('cte -> ID','cte',1,'p_cte','parser.py',231),
  ('cte -> CTEI','cte',1,'p_cte','parser.py',232),
  ('cte -> CTEF','cte',1,'p_cte','parser.py',233),
  ('cte -> CTECHAR','cte',1,'p_cte','parser.py',234),
  ('cte -> bool','cte',1,'p_cte','parser.py',235),
  ('bool -> TRUE','bool',1,'p_bool','parser.py',239),
  ('bool -> FALSE','bool',1,'p_bool','parser.py',240),
  ('main -> MAIN LBRACE statutes_aux RBRACE','main',4,'p_main','parser.py',244),
  ('main -> MAIN LBRACE dec_vars statutes_aux RBRACE','main',5,'p_main','parser.py',245),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',249),
]

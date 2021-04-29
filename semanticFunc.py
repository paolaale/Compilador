# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 30/04/2021

from Classes import Classes
from Functions import Functions
from Vars import Vars

from Quadruple import Quadruple
from collections import deque

# stacks to solve expressions
operatorsStack = deque()
operandsStack = deque()
typesStack = deque()

#Quadruples
quadList = []
jumpsStack = deque()

direcClasses = {} # dictionary of classes
currentClass = ""
currentFunct = ""
lastVarType = ""

stringToWrite = None
quadCounter = 1

# variable de prueba que se borrará después
countOfTemps = 1

# Match type structure where the key is a hashcode of the types
# and the values is an array where index 0 = OA, index 1 = OR, 
# index 2 = OL
typeMatching = {
    'iinntt': ["int", "bool", "error"],
    'afilnott': ["float", "bool", "error"],
    'achinrt': ["error", "error", "error"],
    'aafflloott': ["float", "bool", "error"],
    'aacfhlort': ["error", "error", "error"],
    'aacchhrr': ["error", "error", "error"], #probablemente consideremos relop bool
    'bblloooo': ["error", "error", "bool"]
}

oA = {"+", "-", "*", "/"}
oR = {"<", ">", "<=", ">=", "==", "!="}
oL = {"and", "or"}

# ---------------------- START ADDING ELEMENTS (FUNCT, CLASSES, VARS) ---------------------- #

# function that recieves the name of class, 
# a boolean that represents if is inherit 
# and the name of the parent if is inherit, otherwise recieve None
def addClass(cName, cInherits, cParentName):
    global direcClasses, currentClass, currentFunct
    currentClass = cName 
    currentFunct = ""
    # add to the dictionary of classes the class
    direcClasses[cName] = Classes(cInherits, cParentName) 

# function that recieves the name of the function 
# and the type of return
def addFunction(fName, fType):
    global currentClass, currentFunct
    currentFunct = fName
    # add to dictionary of classes, in the current class the function
    direcClasses[currentClass].c_funcs[fName] = Functions(fType) 

# fucntion that recieves the name and type of the variable
# size 1 that represents number of rows (array)
# size 2 that represents number of columns (matrix)
def addVars(vName, vType, vSize1, vSize2):
    global lastVarType, currentFunct, currentClass
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType

    if currentFunct != "":
        # add to dictionary of classes, in the current class and current function the variables
        direcClasses[currentClass].c_funcs[currentFunct].f_vars[vName] = Vars(vType, vSize1, vSize2)
    else:
        # add to dictionary of classes, in the current class and global variables "fucntion" the variables
        direcClasses[currentClass].c_funcs["vG"].f_vars[vName] = Vars(vType, vSize1, vSize2)

# ---------------------- END ADDING ELEMENTS (FUNCT, CLASSES, VARS) ---------------------- #
    
# ---------------------- START CHECKING MATCH TYPES ---------------------- #

# function to return the key for the typeMatching dictionaru
def matchTypeHashCode(leftOpType, rightOpType):
    return ''.join(sorted(leftOpType + rightOpType))

def typeOfMatch(opSymbol):
    global oA, oR, oL 

    if opSymbol in oA:
        return 0
    elif opSymbol in oR:
        return 1
    else:
        return 2

def isAMatch(leftOpType, opSymbol, rightOpType):

    key = matchTypeHashCode(leftOpType, rightOpType)
    typeOfOP = typeOfMatch(opSymbol)
    resultType = typeMatching[key][typeOfOP]

    return resultType

# ---------------------- END CHECKING MATCH TYPES ---------------------- #

# ---------------------- START CHECKING VARIABLES EXIST ---------------------- #

# Validation method for floats
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

# verify that a variable exists
def getVarType(id):
    global currentFunct, currentClass
   
    if id.isdigit():
        return "int"
    elif isfloat(id):
        return "float"
        
    #aqui probablemente agregar uno para los chars, para que jale la asignacion a = 'b'

    else:   
        scope = existsVar(id)

        if scope == None:
            raise Exception("Variable: ", id, " doesn´t exist")
            return "no existe"
        else:
            #aquí programar para validar que las variables usadas en expresiones sí estén inicializadas
            return direcClasses[currentClass].c_funcs[scope].f_vars[id].v_type
        

def existsVar(id):
    global currentFunct, currentClass

    funcs = direcClasses[currentClass].c_funcs

    if id in funcs[currentFunct].f_vars:
        return currentFunct
    elif id in funcs["vG"].f_vars:
        return "vG"
    else:
        return None

# ---------------------- END CHECKING VARIABLES EXIST ---------------------- #

# ---------------------- START EXPRESSION SOLVING ---------------------- #

def pushOperand(op):
    global operandsStack, quadList

    operandsStack.append(op)
    typesStack.append(getVarType(op))

def pushOperator(op):
    global operatorsStack, typesStack, quadList
    operatorsStack.append(op)

    # if op == "=":
    #     print("----------ASSIGNATION-----------")
    #     quadList = deque()

def pop_op_lop():
    global operatorsStack, operandsStack, quadList, countOfTemps, quadCounter

    # first we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "or" or operatorsStack[-1] == "and"):

        right_op = operandsStack.pop()
        right_op_type = typesStack.pop()
        left_op = operandsStack.pop()
        left_op_type = typesStack.pop()
        operator = operatorsStack.pop()

        operandsMatch = isAMatch(left_op_type, operator, right_op_type)

        if operandsMatch != "error":
            result = "TEMP" + str(countOfTemps)
            countOfTemps += 1

            quadList.append(Quadruple(operator, left_op, right_op, result))
            quadCounter += 1

            operandsStack.append(result)
            typesStack.append(operandsMatch)
    
        else:
            raise Exception("Type mismatch")

# function to pop from the stack "+"" "-""
def pop_op_relop():
    global operatorsStack, operandsStack, quadList, countOfTemps, quadCounter
    
    right_op = operandsStack.pop()
    right_op_type = typesStack.pop()
    left_op = operandsStack.pop()
    left_op_type = typesStack.pop()
    operator = operatorsStack.pop()

    operandsMatch = isAMatch(left_op_type, operator, right_op_type)

    if operandsMatch != "error":
        result = "TEMP" + str(countOfTemps)
        countOfTemps += 1

        quadList.append(Quadruple(operator, left_op, right_op, result))
        quadCounter += 1

        operandsStack.append(result)
        typesStack.append(operandsMatch)
    
    else:
        raise Exception("Type mismatch")

def pop_paren():
    global operatorsStack
    operatorsStack.pop()

# function to pop from the stack "+"" "-""
def pop_op_art_n2():
    global operatorsStack, operandsStack, quadList, countOfTemps, quadCounter

    # first we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "+" or operatorsStack[-1] == "-"):

        right_op = operandsStack.pop()
        right_op_type = typesStack.pop()
        left_op = operandsStack.pop()
        left_op_type = typesStack.pop()
        operator = operatorsStack.pop()

        operandsMatch = isAMatch(left_op_type, operator, right_op_type)

        if operandsMatch != "error":
            result = "TEMP" + str(countOfTemps)
            countOfTemps += 1

            quadList.append(Quadruple(operator, left_op, right_op, result))
            quadCounter += 1

            operandsStack.append(result)
            typesStack.append(operandsMatch)
    
        else:
            raise Exception("Type mismatch")

# function to pop from the stack "*"" "/""
def pop_op_art_n1():
    global operatorsStack, operandsStack, quadList, countOfTemps, quadCounter

    # first we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "*" or operatorsStack[-1] == "/"):

        right_op = operandsStack.pop()
        right_op_type = typesStack.pop()
        left_op = operandsStack.pop()
        left_op_type = typesStack.pop()
        operator = operatorsStack.pop()

        operandsMatch = isAMatch(left_op_type, operator, right_op_type)

        if operandsMatch != "error":
            result = "TEMP" + str(countOfTemps)
            countOfTemps += 1

            quadList.append(Quadruple(operator, left_op, right_op, result))
            quadCounter += 1

            operandsStack.append(result)
            typesStack.append(operandsMatch)
    
        else:
            raise Exception("Type mismatch")

# ---------------------- END EXPRESSION SOLVING ---------------------- #

# ---------------------- START LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

#Aquí el cuadruplo debe quedar como =, TEMP, None, z 
def pop_op_assign():
    global operatorsStack, operandsStack, quadList, quadCounter

    left_op = operandsStack.pop()
    left_op_type = typesStack.pop()
    var_to_assign = operandsStack.pop()
    assignation_type = typesStack.pop()
    operator = operatorsStack.pop()   

    if assignation_type == left_op_type:
        quadList.append(Quadruple(operator, left_op, None, var_to_assign))
        quadCounter += 1
    else:
        raise Exception("Cannot assign variable of type %s with %s" % (assignation_type, left_op_type))

def generateWrite():
    global operandsStack, quadList, stringToWrite, quadCounter, typeStack

    if (stringToWrite != None):
        varToWrite = stringToWrite
        stringToWrite = None
    else:
        varToWrite = operandsStack.pop()
        typesStack.pop()

    quadList.append(Quadruple("WRITE", None, None, varToWrite))
    quadCounter += 1
    

def saveString(s):
    global stringToWrite

    stringToWrite = s

def generateRead():
    global operandsStack, quadList, quadCounter, typesStack

    varToRead = operandsStack.pop()
    typesStack.pop()
    
    quadList.append(Quadruple("READ", None, None, varToRead))
    quadCounter += 1

# ---------------------- END LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# ---------------------- START NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# --- IF --- #

def checkConditionType():
    global quadCounter, jumpsStack, typesStack

    exp_type = typesStack.pop()

    if (exp_type != "bool"):
        raise Exception("Type mismatch")
    else:
        left_op = operandsStack.pop()
        quadList.append(Quadruple("GOTOF", left_op, None, None))
        jumpsStack.append(quadCounter-1)
        quadCounter += 1

def elifCondition():
    global quadCounter, jumpsStack, quadList, typesStack

    """ exp_type = typesStack.pop()

    if (exp_type != "bool"):
        raise Exception("Type mismatch")
    else:
        left_op = operandsStack.pop()
        quadList.append(Quadruple("GOTOF", left_op, None, None))
        quadElif = jumpsStack.pop()
        jumpsStack.append(quadCounter-1)
        quadList[quadElif].tResult = quadCounter-1
        quadCounter += 1 """

def elseCondition():
    global quadCounter, jumpsStack, quadList

    quadElse = jumpsStack.pop()
    quadList.append(Quadruple("GOTO", None, None, None))
    jumpsStack.append(quadCounter-1)
    quadList[quadElse].tResult = quadCounter
    quadCounter += 1

def endIF():
    global quadCounter, jumpsStack, quadList
    
    quadEnd = jumpsStack.pop()
    quadList[quadEnd].tResult = quadCounter-1

# --- END IF --- #

# --- WHILE --- #

# --- END WHILE --- #

# ---------------------- END NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

def printQuadruples():
    global quadList, quadCounter
    i = 0
    for quad in quadList:
        print("Quad ", i, " symbol: ", quad.operation, " left: ", quad.left_op, " right: ", quad.right_op, " temp: ", quad.tResult)
        i += 1
    """ while quadList:
        tempQuad = quadList.popleft()
        print("Quad ", i, " symbol: ", tempQuad.operation, " left: ", tempQuad.left_op, " right: ", tempQuad.right_op, " temp: ", tempQuad.tResult)
        i += 1 """


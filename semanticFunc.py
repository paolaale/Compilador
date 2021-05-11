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

# Dictionaries of classes 
direcClasses = {} 

# Helpers to save classes, functions and vars names
currentClass = ""
currentFunct = ""
lastVarType = ""

# Stacks to solve expressions
operatorsStack = deque()
operandsStack = deque()
typesStack = deque()

# List of quadruples
quadList = []

# Stacks for jumps in the quadruples
jumpsStack = deque()
gotoStack = deque()

# Helpers to fill quadruples
stringToWrite = None
quadCounter = 0
quadElifExpression = None

# Helpers to fill functions
numberOfParams = 0

#!!!! variable de prueba que se borrará después
countOfTemps = 1

# Match type structure where the key is a hashcode of the types 
# and the values is an array where index 0 = OA, index 1 = OR, index 2 = OL
typeMatching = {
    'iinntt': ["int", "bool", "error"],
    'afilnott': ["float", "bool", "error"],
    'achinrt': ["error", "error", "error"],
    'aafflloott': ["float", "bool", "error"],
    'aacfhlort': ["error", "error", "error"],
    'aacchhrr': ["error", "error", "error"], #!!!! probablemente consideremos relop bool
    'bblloooo': ["error", "error", "bool"]
}

# Dictionaries to determine each operator
oA = {"+", "-", "*", "/"}
oR = {"<", ">", "<=", ">=", "==", "!="}
oL = {"and", "or"}

# ---------------------- START ADDING ELEMENTS (FUNCT, CLASSES, VARS) ---------------------- #

# Function that recieves the name of class, 
# a boolean that represents if is inherit 
# and the name of the parent if is inherit, otherwise recieve None
def addClass(cName, cInherits, cParentName):
    global direcClasses, currentClass, currentFunct
    currentClass = cName 
    currentFunct = ""
    # Add to the dictionary of classes the class
    direcClasses[cName] = Classes(cInherits, cParentName) 

# Function that recieves the name of the function 
# and the type of return
def addFunction(fName, fType):
    global currentClass, currentFunct, numberOfParams

    currentFunct = fName
    # Add to dictionary of classes, in the current class the function
    direcClasses[currentClass].c_funcs[fName] = Functions(fType, numberOfParams, None) 

# Function that recieves the name and type of the variable
# size 1 that represents number of rows (array)
# size 2 that represents number of columns (matrix)
def addVars(vName, vType, vSize1, vSize2):
    global lastVarType, currentFunct, currentClass
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType

    if currentFunct != "":
        # Add to dictionary of classes, in the current class and current function the variables
        direcClasses[currentClass].c_funcs[currentFunct].f_vars[vName] = Vars(vType, vSize1, vSize2)
    else:
        # Add to dictionary of classes, in the current class and global variables "function" the variables
        direcClasses[currentClass].c_funcs["vG"].f_vars[vName] = Vars(vType, vSize1, vSize2)

def addParam(pName, pType, pSize1, pSize2):
    global currentFunct, currentClass, numberOfParams
    
    # Add to dictionary of classes, in the current class and current function the parameters
    direcClasses[currentClass].c_funcs[currentFunct].f_vars[pName] = Vars(pType, pSize1, pSize2)
    numberOfParams += 1

# ---------------------- END ADDING ELEMENTS (FUNCT, CLASSES, VARS) ---------------------- #
    
# ---------------------- START CHECKING MATCH TYPES ---------------------- #

# Function that recieves two strings that represents the operands type
# and returns the key for the typeMatching dictionary
def matchTypeHashCode(leftOpType, rightOpType):
    return ''.join(sorted(leftOpType + rightOpType))

# Function that recieves the symbol, 
# looks for them in each operator dictionary
# and returns if symbol is arithmetic, logical or relational
def typeOfMatch(opSymbol):
    global oA, oR, oL 

    if opSymbol in oA:
        return 0
    elif opSymbol in oR:
        return 1
    else:
        return 2

# Function that recieves the operands and operator
# uses the functions established before and 
# returns the type of match
def isAMatch(leftOpType, opSymbol, rightOpType):

    key = matchTypeHashCode(leftOpType, rightOpType)
    typeOfOP = typeOfMatch(opSymbol)
    resultType = typeMatching[key][typeOfOP]

    return resultType

# ---------------------- END CHECKING MATCH TYPES ---------------------- #

# ---------------------- START CHECKING VARIABLES EXIST ---------------------- #

# Function that recieves a value 
# and validates if is a float
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

# Function that recieves an id and looks for them 
# in the currents function or in the globals
# returns the function where is found or None
def existsVar(id):
    global currentFunct, currentClass

    funcs = direcClasses[currentClass].c_funcs

    if id in funcs[currentFunct].f_vars:
        return currentFunct
    elif id in funcs["vG"].f_vars:
        return "vG"
    else:
        return None

# Function that recieves an id and verify that the variable exists 
# if found returns the variable type, if not returns an exception
def getVarType(id):
    global currentFunct, currentClass
   
    if id.isdigit():
        return "int"
    elif isfloat(id):
        return "float"     
    #!!!! aqui probablemente agregar uno para los chars, para que jale la asignacion a = 'b'
    else:   
        scope = existsVar(id) # call to previous function

        if scope == None:
            raise Exception("Variable: ", id, " doesn´t exist")
            return "no existe"
        else:
            #!!! aquí programar para validar que las variables usadas en expresiones sí estén inicializadas
            return direcClasses[currentClass].c_funcs[scope].f_vars[id].v_type

# ---------------------- END CHECKING VARIABLES EXIST ---------------------- #

# ---------------------- START EXPRESSION SOLVING ---------------------- #

# Function to push the operand and its type in their corresponding stacks
def pushOperand(op):
    global operandsStack, quadList
    operandsStack.append(op)
    typesStack.append(getVarType(op))

# Function to push the operator to the operatorsStack
def pushOperator(op):
    global operatorsStack, typesStack, quadList
    operatorsStack.append(op)

# function to validate and create a quadruaple of logical operators
def pop_op_lop():
    global operatorsStack

    # First we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "or" or operatorsStack[-1] == "and"):
        generateExpQuad()

# function to validate and create a quadruaple of relational operators
def pop_op_relop():
    generateExpQuad()

# function to pop from our OperatorsStack our fake background when found "("
def pop_paren():
    global operatorsStack
    operatorsStack.pop()

# Function to pop from the stack "+"" "-""
def pop_op_art_n2():
    global operatorsStack

    # First we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "+" or operatorsStack[-1] == "-"):
        generateExpQuad()

# Function to pop from the stack "*"" "/""
def pop_op_art_n1():
    global operatorsStack

    # First we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "*" or operatorsStack[-1] == "/"):
        generateExpQuad()

# Function to generate th corresponding quadruple of an expression
def generateExpQuad():
    global operatorsStack, operandsStack, quadList, countOfTemps, quadCounter, typesStack

    right_op = operandsStack.pop()
    right_op_type = typesStack.pop()
    left_op = operandsStack.pop()
    left_op_type = typesStack.pop()
    operator = operatorsStack.pop()

    operandsMatch = isAMatch(left_op_type, operator, right_op_type) # get the matching compatibility of both operands types

    # If operands types are compatible, generate quadruple and update quadcounter, else, throw exception
    if operandsMatch != "error":
        result = "TEMP" + str(countOfTemps)
        countOfTemps += 1

        quadCounter += 1
        quadList.append(Quadruple(operator, left_op, right_op, result))

        operandsStack.append(result)
        typesStack.append(operandsMatch)
    
    else:
        raise Exception("Type mismatch")

# ---------------------- END EXPRESSION SOLVING ---------------------- #

# ---------------------- START LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# function to generate que assignation and add it to out quadList
def pop_op_assign():
    global operatorsStack, operandsStack, quadList, quadCounter

    left_op = operandsStack.pop()
    left_op_type = typesStack.pop()
    var_to_assign = operandsStack.pop()
    assignation_type = typesStack.pop()
    operator = operatorsStack.pop()   
    
    # Validate that the type of the exp result is the same of the variable to assign
    if assignation_type == left_op_type:
        quadCounter += 1
        quadList.append(Quadruple(operator, left_op, None, var_to_assign))
    else:
        raise Exception("Cannot assign variable of type %s with %s" % (assignation_type, left_op_type))

# Function that saves the string to write
def saveString(s):
    global stringToWrite

    stringToWrite = s

# Function that generates the write quad
def generateWrite():
    global operandsStack, quadList, stringToWrite, quadCounter, typeStack

    # If there is a string to write gets it from helper 
    if (stringToWrite != None):
        varToWrite = stringToWrite
        stringToWrite = None
    # Or if it is an expression gets it from the operands stack
    else:
        varToWrite = operandsStack.pop()
        typesStack.pop()

    quadCounter += 1
    quadList.append(Quadruple("WRITE", None, None, varToWrite))

# Function that generates the read quad
def generateRead():
    global operandsStack, quadList, quadCounter, typesStack

    varToRead = operandsStack.pop()
    typesStack.pop()
    
    quadCounter += 1
    quadList.append(Quadruple("READ", None, None, varToRead))

# ---------------------- END LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# ---------------------- START NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# --- IF --- #

# Function that generates the if GOTOF quad 
# only if the there is a match type otherwise raise exception 
def ifCondition():
    global quadCounter, jumpsStack, typesStack

    exp_type = typesStack.pop()

    if (exp_type != "bool"):
        raise Exception("Type mismatch")
    else:
        left_op = operandsStack.pop()
        quadCounter += 1
        quadList.append(Quadruple("GOTOF", left_op, None, None))
        jumpsStack.append(quadCounter-1)

# Function that generates the if GOTO quad 
# only if there is an elif condition 
def elifExpression():
    global quadElifExpression, quadCounter

    quadCounter += 1 
    quadList.append(Quadruple("GOTO", None, None, None))
    quadElifExpression = quadCounter
    gotoStack.append(quadCounter-1)

# Function that generates the elif GOTOF quad 
# only if the there is a match type otherwise raise exception
def elifCondition():
    global quadCounter, jumpsStack, quadList, typesStack, quadElifExpression

    exp_type = typesStack.pop()

    if (exp_type != "bool"):
        raise Exception("Type mismatch")
    else:
        left_op = operandsStack.pop()
        quadCounter += 1 
        quadList.append(Quadruple("GOTOF", left_op, None, None))
        quadElif = jumpsStack.pop()
        jumpsStack.append(quadCounter-1)
        quadList[quadElif].tResult = quadElifExpression

# Function that generates the else GOTO quad 
def elseCondition():
    global quadCounter, jumpsStack, quadList

    quadElse = jumpsStack.pop()
    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, None))
    jumpsStack.append(quadCounter-1)
    quadList[quadElse].tResult = quadCounter

# Function that fills the empty GOTO quads left on the if statement 
def endIF():
    global quadCounter, jumpsStack, quadList, gotoStack
    
    quadEnd = jumpsStack.pop()
    quadList[quadEnd].tResult = quadCounter

    while gotoStack:
        quadEnd = gotoStack.pop()
        quadList[quadEnd].tResult = quadCounter

# --- END IF --- #

# --- WHILE --- #

# Function that saves the quad where the expression of the while starts on the stack
def whileJump():
    global quadCounter, jumpsStack
    jumpsStack.append(quadCounter)

# Function that generates the while GOTOF quad 
# only if the there is a match type otherwise raise exception
def whileCondition():
    global quadCounter, typesStack, quadList, operandsStack, jumpsStack

    resultType = typesStack.pop()

    if resultType != "bool":
        raise Exception("Type mismatch. Expecting bool")
    else:
        expResult = operandsStack.pop()
        quadCounter += 1
        quadList.append(Quadruple("GOTOF", expResult, None, None))
        jumpsStack.append(quadCounter - 1)

# Function that generates the while GOTO quad 
# to return to the expression and check it again (cycle)
def endWhile():
    global quadCounter, typesStack, quadList, operandsStack, jumpsStack

    endWhile = jumpsStack.pop()
    whileReturnQuad = jumpsStack.pop()
    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, whileReturnQuad))
    quadList[endWhile].tResult = quadCounter

# --- END WHILE --- #

# --- FOR --- #

# Function that saves the quad where the expression of the for starts on the stack
def forJump():
    global quadCounter, jumpsStack
    jumpsStack.append(quadCounter)

# Function that generates the for GOTOF quad 
# only if the there is a match type otherwise raise exception
def forCondition():
    global quadCounter, jumpsStack, typesStack

    exp_type = typesStack.pop()

    if (exp_type != "bool"):
        raise Exception("Type mismatch")
    else:
        left_op = operandsStack.pop()
        quadCounter += 1
        quadList.append(Quadruple("GOTOF", left_op, None, None))
        jumpsStack.append(quadCounter-1)

# Function that generates the for GOTO quad 
# to return to the expression and check it again (cycle)
def endFor():
    global quadCounter, jumpsStack, quadList, gotoStack
    
    quadCounter += 1
    quadEnd = jumpsStack.pop()
    returnFor = jumpsStack.pop()
    quadList.append(Quadruple("GOTO", None, None, returnFor))
    quadList[quadEnd].tResult = quadCounter

# --- END FOR --- #

# ---------------------- END NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# ---------------------- FUNCTIONS ---------------------- #

def existFunction(functionCall):
    global direcClasses

    if functionCall not in direcClasses["main"].c_funcs:
        raise Exception("Function not found")

def insertParams():
    global numberOfParams, currentClass, currentFunct, direcClasses

    direcClasses[currentClass].c_funcs[currentFunct].f_number_params = numberOfParams
    numberOfParams = 0

def startFunction():
    global currentClass, currentFunct, direcClasses

    direcClasses[currentClass].c_funcs[currentFunct].f_start_quadruple = quadCounter

def endFunction():
    global quadCounter

    quadCounter += 1
    quadList.append(Quadruple("END FUNCTION", None, None, None))
    #!!!! matar a current directorio de variables
    #!!!! guardar numero de temporales usados


#---------------------- END FUNCTIONS ---------------------- #

#---------------------- MAIN ---------------------- #

def checkInit():
    global quadCounter, quadList, jumpsStack

    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, None))
    jumpsStack.append(quadCounter-1)

def startInit():
    global quadCounter, quadList, jumpsStack

    quadCounter += 1
    quadInit = jumpsStack.pop()
    quadList[quadInit].tResult = quadCounter-1

#---------------------- END MAIN ---------------------- #

# ---------------------- PROGRAM END ---------------------- #

# Function that generates the END of the program quad
def endProgram():
    global quadList

    quadList.append(Quadruple("END PROGRAM", None, None, None))


#!!!! se borrara después  
def printQuadruples():
    global quadList, quadCounter
    i = 0
    for quad in quadList:
        print("Quad ", i, " symbol: ", quad.operation, " left: ", quad.left_op, " right: ", quad.right_op, " temp: ", quad.tResult)
        i += 1


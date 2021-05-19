# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 14/05/2021

from Classes import Classes
from Functions import Functions
from Vars import Vars

from Quadruple import Quadruple
from collections import deque

import MemoryDispatcher as mD

#test = MemoryDispatcher()

# Dictionaries of classes 
direcClasses = {} 

# Helpers to save classes, functions and vars names
currentClass = ""
currentFunct = "vG"
lastVarType = ""

# Stacks to solve expressions
operatorsStack = deque()
operandsStack = deque()
typesStack = deque()

# List of quadruples
quadList = []

# List of quadruples MEMORY
quadMEM = []

# Temps Memory directions Dictionary
directTemp = {}

#Temps Memory Constants
directConstants = {}

# Stacks for jumps in the quadruples
jumpsStack = deque()
gotoStack = deque()

# Helpers to fill quadruples
stringToWrite = None
quadCounter = 0
quadElifExpression = None

# Helpers to fill functions
numberOfParams = 0
functionToCall = ""
numberOfArgs = 0
numberOfVars = {"int": 0, "float": 0, "char": 0}
numberOfTemps = {"int": 0, "float": 0, "char": 0, "bool": 0}

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
    mD.reset_global_space()
    currentClass = cName 
    currentFunct = "vG"
    # Add to the dictionary of classes the class
    direcClasses[cName] = Classes(cInherits, cParentName) 

# Function that recieves the name of the function 
# and the type of return
def addFunction(fName, fType):
    global currentClass, currentFunct, numberOfParams
    mD.reset_local_space()
    currentFunct = fName
    directTemp = {}
    # Add to dictionary of classes, in the current class the function
    direcClasses[currentClass].c_funcs[fName] = Functions(fType, [], numberOfParams, None) 

# Function that recieves the name and type of the variable
# size 1 that represents number of rows (array)
# size 2 that represents number of columns (matrix)
def addVars(vName, vType, vSize1, vSize2):
    global lastVarType, currentFunct, currentClass

    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType


    # Check variable wasn't already declare in the function
    if vName not in direcClasses[currentClass].c_funcs[currentFunct].f_vars:

        # To know how many spaces it will take on the memory
        memorySize = abs(int(vSize1) * int(vSize2))
        # Add to dictionary of classes, in the current class and current function the variables
        direcClasses[currentClass].c_funcs[currentFunct].f_vars[vName] = Vars(vType, vSize1, vSize2, mD.get_space_avail(currentFunct, vType, memorySize))
        numberOfVars[vType] += 1
    else:
        raise Exception("Variable '" + vName + "' already exist")

# Function that recieves the name and type of the parameter of the function
# size 1 that represents number of rows (array)
# size 2 that represents number of columns (matrix)
def addParam(pName, pType, pSize1, pSize2):
    global currentFunct, currentClass, numberOfParams
    
    # To know how many spaces it will take on the memory
    memorySize = abs(int(pSize1) * int(pSize2))

    # Add to dictionary of classes, in the current class and current function the parameters
    direcClasses[currentClass].c_funcs[currentFunct].f_vars[pName] = Vars(pType, pSize1, pSize2, mD.get_space_avail("local", pType, memorySize))
    numberOfVars[pType] += 1
    # Add to dictionary of classes, in the current class and current function the parameter type in an array
    direcClasses[currentClass].c_funcs[currentFunct].f_params_type.append(pType)
    # Count the numer of parameters in current function for later use
    numberOfParams += 1 

def convertMatrixToColumn(): #!!!! recibe los tamaños
    print("hola")

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
    global currentFunct, currentClass, directConstants
   
    if id.isdigit():
        if id not in directConstants:
            directConstants[id] = mD.get_space_avail("const", "int", 1)
        return "int"
    elif isfloat(id):
        if id not in directConstants:
            directConstants[id] = mD.get_space_avail("float", "int", 1)
        return "float"     
    #!!!! aqui probablemente agregar uno para los chars, para que jale la asignacion a = 'b'
    else:   
        scope = existsVar(id) # call to previous function

        if scope == None:
            raise Exception("Variable '" + id + "' was not declare.")
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
    global operatorsStack, operandsStack, quadList, quadMEM, countOfTemps, quadCounter, typesStack, numberOfTemps, directConstants

    rightOp = operandsStack.pop()
    rightOpType = typesStack.pop()
    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    operator = operatorsStack.pop()

    operandsMatch = isAMatch(leftOpType, operator, rightOpType) # get the matching compatibility of both operands types

    # If operands types are compatible, generate quadruple and update quadcounter, else, throw exception
    if operandsMatch != "error":
        result = "TEMP" + str(countOfTemps)
        tempResult = mD.get_space_avail("temp", operandsMatch, 1);
        directTemp[result] = tempResult

        memRefLeftOp = getMemoryRef(leftOp)
        memRefRightOp = getMemoryRef(rightOp)

        countOfTemps += 1

        quadCounter += 1

        quadList.append(Quadruple(operator, leftOp, rightOp, result))
        quadMEM.append(Quadruple(operator, memRefLeftOp, memRefRightOp, tempResult))

        operandsStack.append(result)
        typesStack.append(operandsMatch)

        numberOfTemps[operandsMatch] += 1
    
    else:
        raise Exception("Type mismatch")

# ---------------------- END EXPRESSION SOLVING ---------------------- #

# ---------------------- START LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# function to generate que assignation and add it to out quadList
def pop_op_assign():
    global operatorsStack, operandsStack, quadList, quadCounter, quadMEM

    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    varToAssign = operandsStack.pop()
    assignationType = typesStack.pop()
    operator = operatorsStack.pop()   
    memRefLeftOp = getMemoryRef(leftOp)
    memVarToAsign = getMemoryRef(varToAssign)
    # Validate that the type of the exp result is the same of the variable to assign
    if assignationType == leftOpType:
        quadCounter += 1
        quadList.append(Quadruple(operator, leftOp, None, varToAssign))
        quadMEM.append(Quadruple(operator, memRefLeftOp, None, memVarToAsign))
    else:
        raise Exception("Cannot assign variable of type %s with %s" % (assignationType, leftOpType))

# Function that saves the string to write
def saveString(s):
    global stringToWrite
    print("GOKUUUUU: ", s);
    stringToWrite = s

# Function that generates the write quad
def generateWrite():
    global operandsStack, quadList, stringToWrite, quadCounter, typeStack, quadMEM

    
    # If there is a string to write gets it from helper 
    if (stringToWrite != None):
        varToWrite = stringToWrite
        memVarToWrite = stringToWrite
        stringToWrite = None

    # Or if it is an expression gets it from the operands stack
    else:
        varToWrite = operandsStack.pop()
        typesStack.pop()
        memVarToWrite = getMemoryRef(varToWrite)

    quadCounter += 1
    quadList.append(Quadruple("WRITE", None, None, varToWrite))
    quadMEM.append(Quadruple("WRITE", None, None, memVarToWrite))

# Function that generates the read quad
def generateRead():
    global operandsStack, quadList, quadCounter, typesStack, quadMEM

    varToRead = operandsStack.pop()
    memVarToRead = getMemoryRef(varToRead)
    typesStack.pop()
    
    quadCounter += 1
    quadList.append(Quadruple("READ", None, None, varToRead))
    quadMEM.append(Quadruple("READ", None, None, memVarToRead))

# ---------------------- END LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# ---------------------- START NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# --- IF --- #

# Function that generates the if GOTOF quad 
# only if the there is a match type otherwise raise exception 
def ifCondition():
    global quadCounter, jumpsStack, typesStack

    expType = typesStack.pop()

    if (expType != "bool"):
        raise Exception("Type mismatch")
    else:
        leftOp = operandsStack.pop()
        memLeftOp = getMemoryRef(leftOp)
        quadCounter += 1
        quadList.append(Quadruple("GOTOF", leftOp, None, None))
        quadMEM.append(Quadruple("GOTOF", memLeftOp, None, None))
        print("QUADQUAD", quadCounter-1);
        jumpsStack.append(quadCounter-1)

# Function that generates the if GOTO quad 
# only if there is an elif condition 
def elifExpression():
    global quadElifExpression, quadCounter, quadMEM, quadList

    quadCounter += 1 
    quadList.append(Quadruple("GOTO", None, None, None))
    quadMEM.append(Quadruple("GOTO", None, None, None))
    quadElifExpression = quadCounter
    gotoStack.append(quadCounter-1)

# Function that generates the elif GOTOF quad 
# only if the there is a match type otherwise raise exception
def elifCondition():
    global quadCounter, jumpsStack, quadList, typesStack, quadElifExpression, quadMEM

    expType = typesStack.pop()

    if (expType != "bool"):
        raise Exception("Type mismatch")
    else:
        leftOp = operandsStack.pop()
        memLeftOp = getMemoryRef(leftOp)
        quadCounter += 1 
        quadList.append(Quadruple("GOTOF", leftOp, None, None))
        quadMEM.append(Quadruple("GOTOF", memLeftOp, None, None))
        quadElif = jumpsStack.pop()
        jumpsStack.append(quadCounter-1)
        quadList[quadElif].tResult = quadElifExpression
        quadMEM[quadElif].tResult = quadElifExpression

# Function that generates the else GOTO quad 
def elseCondition():
    global quadCounter, jumpsStack, quadList, quadMEM

    quadElse = jumpsStack.pop()
    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, None))
    quadMEM.append(Quadruple("GOTO", None, None, None))
    jumpsStack.append(quadCounter-1)
    quadList[quadElse].tResult = quadCounter
    quadMEM[quadElse].tResult = quadCounter

# Function that fills the empty GOTO quads left on the if statement 
def endIF():
    global quadCounter, jumpsStack, quadList, gotoStack, quadMEM
    
    quadEnd = jumpsStack.pop()
    quadList[quadEnd].tResult = quadCounter
    quadMEM[quadEnd].tResult = quadCounter

    while gotoStack:
        quadEnd = gotoStack.pop()
        quadList[quadEnd].tResult = quadCounter
        quadMEM[quadEnd].tResult = quadCounter

# --- END IF --- #

# --- WHILE --- #

# Function that saves the quad where the expression of the while starts on the stack
def whileJump():
    global quadCounter, jumpsStack
    jumpsStack.append(quadCounter)

# Function that generates the while GOTOF quad 
# only if the there is a match type otherwise raise exception
def whileCondition():
    global quadCounter, typesStack, quadList, operandsStack, jumpsStack, quadMEM

    resultType = typesStack.pop()

    if resultType != "bool":
        raise Exception("Type mismatch. Expecting bool")
    else:
        expResult = operandsStack.pop()
        memExpResult = getMemoryRef(expResult)
        quadCounter += 1
        quadList.append(Quadruple("GOTOF", expResult, None, None))
        quadMEM.append(Quadruple("GOTOF", memExpResult, None, None))
        jumpsStack.append(quadCounter - 1)

# Function that generates the while GOTO quad 
# to return to the expression and check it again (cycle)
def endWhile():
    global quadCounter, typesStack, quadList, operandsStack, jumpsStack, quadMEM

    endWhile = jumpsStack.pop()
    whileReturnQuad = jumpsStack.pop()
    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, whileReturnQuad))
    quadMEM.append(Quadruple("GOTO", None, None, whileReturnQuad))
    quadList[endWhile].tResult = quadCounter
    quadMEM[endWhile].tResult = quadCounter

# --- END WHILE --- #

# --- FOR --- #

# Function that saves the quad where the expression of the for starts on the stack
def forJump():
    global quadCounter, jumpsStack
    jumpsStack.append(quadCounter)

# Function that generates the for GOTOF quad 
# only if the there is a match type otherwise raise exception
def forCondition():
    global quadCounter, jumpsStack, typesStack, quadList, quadMEM

    expType = typesStack.pop()

    if (expType != "bool"):
        raise Exception("Type mismatch")
    else:
        leftOp = operandsStack.pop()
        memLeftOp = getMemoryRef(leftOp)
        quadCounter += 1
        quadList.append(Quadruple("GOTOF", leftOp, None, None))
        quadMEM.append(Quadruple("GOTOF", memLeftOp, None, None))
        jumpsStack.append(quadCounter-1)

# Function that generates the for GOTO quad 
# to return to the expression and check it again (cycle)
def endFor():
    global quadCounter, jumpsStack, quadList, gotoStack, quadMEM
    
    quadCounter += 1
    quadEnd = jumpsStack.pop()
    returnFor = jumpsStack.pop()
    quadList.append(Quadruple("GOTO", None, None, returnFor))
    quadMEM.append(Quadruple("GOTO", None, None, returnFor))
    quadList[quadEnd].tResult = quadCounter
    quadMEM[quadEnd].tResult = quadCounter

# --- END FOR --- #

# ---------------------- END NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# ---------------------- FUNCTIONS ---------------------- #

# Function that recieves the name of the function called and verify that exists
# if not, an exception is shown
def existFunction(functionCall):
    global direcClasses, functionToCall

    if functionCall not in direcClasses["main"].c_funcs:
        raise Exception("Function not found")
    else:
        functionToCall = functionCall

# Function that generates the Activation Record expansion new size
def eraSizeFunction():
    global quadCounter, quadList, functionToCall, quadMEM

    quadCounter += 1
    quadList.append(Quadruple("ERA", None, None, functionToCall))
    quadMEM.append(Quadruple("ERA", None, None, functionToCall))

# Function that recieves the argument that will be send to the parameter of the function
def argFunction():
    global quadCounter, quadList, operandsStack, typesStack, functionToCall, numberOfArgs, quadMEM

    numberOfArgs += 1
    argument = operandsStack.pop()
    argumentType = typesStack.pop()
    
    memArgument = getMemoryRef(argument)

    # Checks that the function to be called has parameters
    if len(direcClasses["main"].c_funcs[functionToCall].f_params_type) >= numberOfArgs:
        # Check the parameter type is equal to the argument type 
        if direcClasses["main"].c_funcs[functionToCall].f_params_type[numberOfArgs-1] == argumentType:
            quadCounter += 1
            quadList.append(Quadruple("PARAM", argument, None, numberOfArgs-1))
            quadMEM.append(Quadruple("PARAM", memArgument, None, numberOfArgs-1))
        else:
            raise Exception("Type mismatch")
    else:
        # if there are more arguments sent than parameters recieving in the function generate exception
        raise Exception("Number of arguments mismatch")

# Function that indicates where the code of the function called starts
def gosubFunction():
    global quadCounter, quadList, functionToCall, numberOfArgs, quadMEM

    nP = direcClasses["main"].c_funcs[functionToCall].f_number_params

    # Check the number of parameters and arguments match
    if numberOfArgs == nP:
        quadCounter += 1
        functionStart = direcClasses["main"].c_funcs[functionToCall].f_start_quadruple
        quadList.append(Quadruple("GOSUB", None, None, functionStart))
        quadMEM.append(Quadruple("GOSUB", None, None, functionStart))
        functionToCall = "" 
        numberOfArgs = 0
    else:
        raise Exception("Number of arguments mismatch")

# Function that saves how many parameters the function has
def insertParams():
    global numberOfParams, currentClass, currentFunct, direcClasses

    direcClasses[currentClass].c_funcs[currentFunct].f_number_params = numberOfParams
    numberOfParams = 0

# Function that saves the quadruple where the code of the function starts
def startFunction():
    global currentClass, currentFunct, direcClasses

    direcClasses[currentClass].c_funcs[currentFunct].f_start_quadruple = quadCounter

def saveLocalVars():
    global numberOfVars

    #!!!! calcula la memoria
    print("funct var types count", numberOfVars)
    numberOfVars = {"int": 0, "float": 0, "char": 0}

def saveTempVars():
    global numberOfTemps

    #!!!! calcula la memoria
    print("funct temp var types count", numberOfTemps)
    numberOfTemps = {"int": 0, "float": 0, "char": 0, "bool": 0}

# Function that indicates where the function end and release the cuurent var table
def endFunction():
    global quadCounter, quadList, countOfTemps, quadMEM

    quadCounter += 1
    quadList.append(Quadruple("END FUNCTION", None, None, None))
    quadMEM.append(Quadruple("END FUNCTION", None, None, None))
    countOfTemps = 1
    #!!!! matar a current directorio de variables
    #!!!! guardar numero de temporales usados

#---------------------- END FUNCTIONS ---------------------- #

#---------------------- MAIN ---------------------- #

# Function that generates the quadruple at the start of the program to go to the init function
def checkInit():
    global quadCounter, quadList, jumpsStack, quadMEM
    jumpsStack.append(quadCounter)
    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, None))
    quadMEM.append(Quadruple("GOTO", None, None, None))
    

# Function that saves where the code of the init function starts
def startInit():
    global quadCounter, quadList, jumpsStack, quadMEM

    quadInit = jumpsStack.pop()
    quadList[quadInit].tResult = quadCounter
    quadMEM[quadInit].tResult = quadCounter

#---------------------- END MAIN ---------------------- #

# ---------------------- PROGRAM END ---------------------- #

# Function that generates the END of the program quad
def endProgram():
    global quadList, quadMEM

    quadList.append(Quadruple("END PROGRAM", None, None, None))
    quadMEM.append(Quadruple("END PROGRAM", None, None, None))

#---------------------- MEMORY REFERENCES START ---------------------- #
def getMemoryRef(op):
    global direcClasses, directConstants, directTemp, currentClass

    scopeOfOp = ""

    if op in directConstants:
        return directConstants[op]
    elif op in directTemp:
        return directTemp[op]
    else:
        scopeOfOp = existsVar(op)

    return direcClasses[currentClass].c_funcs[scopeOfOp].f_vars[op].memRef;
#---------------------- MEMORY REFERENCES END ---------------------- #


#!!!! se borrara después  
def printQuadruples():
    global quadList, quadCounter
    i = 0
    for quad in quadList:
        print("Quad ", i, " symbol: ", quad.operation, " left: ", quad.left_op, " right: ", quad.right_op, " temp: ", quad.tResult)
        i += 1


def printMemoryQuadruples():
    global quadMEM, quadCounter
    i = 0
    for quad in quadMEM:
        print("Quad ", i, " symbol: ", quad.operation, " left: ", quad.left_op, " right: ", quad.right_op, " temp: ", quad.tResult)
        i += 1
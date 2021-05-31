# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 21/05/2021

from Classes import Classes
from Functions import Functions
from Vars import Vars

from Quadruple import Quadruple
from collections import deque

import MemoryDispatcher as mD

# Dictionary of classes 
direcClasses = {} 
# Dictionary of memory addresses of temps 
directTemp = {}
# Dictionary of memory addresses of constants temps 
directConstants = {}
# Dictionary of memory addresses of objects instances 
directInstances = {}

# Helpers to save classes, functions and vars names
currentClass = ""
currentFunct = "vG"
lastVarType = ""

# Stacks to solve expressions
operatorsStack = deque()
operandsStack = deque()
typesStack = deque()
objVarsMemRef = deque()

# Stacks for jumps in the quadruples
jumpsStack = deque()
gotoStack = deque()

# Stack of array access
accesArrayStack = deque()

# List of quadruples
quadList = []
# List of quadruples with memory addresses
quadMEM = []
# List of params per function
functParams = []

# Helpers to fill quadruples
stringToWrite = None
quadCounter = 0
quadElifExpression = None
direcOperators = {
                    "+": 1, "-": 2, "*": 3, "/": 4, "=": 5, 
                    "and": 6, "or": 7, ">": 8, ">=": 9, "<": 10, 
                    "<=": 11, "==": 12, "!=": 13, "VERIFY": 14, "WRITE": 15, 
                    "READ": 16, "GOTO": 17, "GOTOF": 18, "ERA": 19, "PARAM": 20, 
                    "GOSUB": 21, "RETURN": 22, "END FUNCTION": 23, "BASEADDRESS": 24,
                    "ERAC": 25, "ERACM": 26, "GOSUBCM": 27, "END PROGRAM": 28
                }

# Helpers to fill functions
numberOfParams = 0
functionToCall = ""
numberOfArgs = 0

# Helpers for data structures
currentDataType = 0
currentDataLowerLimit = 0
currentMatrixSize = 0

# Helpers for classes
currentObject = ""
methodToCall = ""
classToAccess = ""

# Counter of temporal variables
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
    
    # Before another class comes, reset the memory addresses
    mD.reset_global_space()

    currentClass = cName 
    currentFunct = "vG"

    # Check class wasn't already declare
    if cName not in direcClasses:
        # Add to the dictionary of classes the class
        direcClasses[cName] = Classes(cInherits, cParentName) 
    else:
         raise Exception("Class '" + cName + "' already exist")

# Function that recieves the name of the function 
# and the type of function 
def addFunction(fName, fType):
    global currentClass, currentFunct, numberOfParams
    
    currentFunct = fName
    directTemp = {} #!!!! ?? que hace

    # Check function wasn't already declare in the class
    if fName not in direcClasses[currentClass].c_funcs:
        # Add to dictionary of classes, in the current class the function
        direcClasses[currentClass].c_funcs[fName] = Functions(fType, [], numberOfParams, None) 

        if fType != "void":
            # Because has a return, we add a variable to the global variables that will represent the returnable variable
            direcClasses[currentClass].c_funcs["vG"].f_vars[currentFunct] = Vars(fType, -1, -1, mD.get_space_avail("vG", fType, 1))
    else:
         raise Exception("Function '" + fName + "' already exist")

# Function that recieves the name and type of the variable
# size 1 that represents number of rows (array)
# size 2 that represents number of columns (matrix)
def addVars(vName, vType, vSize1, vSize2):
    global lastVarType, currentFunct, currentClass, quadCounter

    # It means in the declaration there are vars of the same type, so we get the lastVarType
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType
    
    # Check variable wasn't already declare in the function
    if vName not in direcClasses[currentClass].c_funcs[currentFunct].f_vars:

        # Add the size of the first dimension of the var in the dictionary of constants
        if isInt(vSize1) and vSize1 not in directConstants:
            directConstants[vSize1] = mD.get_space_avail("const", "int", 1)
        
        # Add the size of the second dimension of the var in the dictionary of constants
        if isInt(vSize2) and vSize2 not in directConstants:
            directConstants[vSize2] = mD.get_space_avail("const", "int", 1)

        # To know how many spaces it will take on the memory
        memorySize = abs(int(vSize1) * int(vSize2))

        # Memory reference of variable
        memRef = mD.get_space_avail(currentFunct, vType, memorySize)

        # Add to dictionary of classes, in the current class and current function the variables
        direcClasses[currentClass].c_funcs[currentFunct].f_vars[vName] = Vars(vType, vSize1, vSize2, memRef)

    else:
        raise Exception("Variable '" + vName + "' already exist")
    
    # If variables is an object creates the quadruple for the class activation memory record
    if vType != "int" and vType != "float" and vType != "char":
        
        # Check the class of the object exist
        if vType in direcClasses:
            quadCounter += 1
            quadList.append(Quadruple("ERAC", None, None, vType))
            quadMEM.append(Quadruple(direcOperators["ERAC"], None, None, memRef))
        else:
            raise Exception("Class '" + vType + "' doest not exist")
        

# Function that recieves the name and type of the parameter of the function
# size 1 that represents number of rows (array)
# size 2 that represents number of columns (matrix)
def addParam(pName, pType, pSize1, pSize2):
    global currentFunct, currentClass, numberOfParams
    
    # To know how many spaces it will take on the memory
    memorySize = abs(int(pSize1) * int(pSize2))

    # Create the memory reference (Memref) for the parameter
    paramMemRef = mD.get_space_avail("local", pType, memorySize)

    # Add to dictionary of classes, in the current class and current function the parameters
    direcClasses[currentClass].c_funcs[currentFunct].f_vars[pName] = Vars(pType, pSize1, pSize2, paramMemRef)

    # Add to dictionary of classes, in the current class and current function the parameter type in an array
    direcClasses[currentClass].c_funcs[currentFunct].f_params_type.append(pType)

    # Add the memory referece of the Param to the list of MemRefs of params of the function
    direcClasses[currentClass].c_funcs[currentFunct].f_params_memRefs.append(paramMemRef)

    # Count the number of parameters in current function for later use
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
# and validates if is a int
def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function that recieves a value 
# and validates if is a float
def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Function that recieves a value 
# and validates if is a char
def isChar(value):
    if len(value) == 3 and (value[0] == "'" and value[2] == "'"):
        return True
    else:
        return False

# Function that recieves an id and looks for them 
# in the function to check or in the globals of the class to check
# and returns the function where is found or None
def existsVar(id, classToCheck, funcToCheck):

    funcs = direcClasses[classToCheck].c_funcs

    if id in funcs[funcToCheck].f_vars:
        return funcToCheck
    elif id in funcs["vG"].f_vars:
        return "vG"
    else:
        return None

# Function that recieves an id and checks if is a constant or 
# if is a variable then check if exist 
# if found returns the type, if not returns an exception
def getVarType(id):
    global currentFunct, currentClass, directConstants
   
    if isInt(id):
        # Added it to the constants if is not already in it
        if id not in directConstants:
            directConstants[id] = mD.get_space_avail("const", "int", 1)
        return "int"
    elif isFloat(id):
        # Added it to the constants if is not already in it
        if id not in directConstants:
            directConstants[id] = mD.get_space_avail("const", "float", 1)
        return "float"
    elif isChar(id):
        # Added it to the constants if is not already in it
        if id not in directConstants:
            id = id.replace("'", '')
            directConstants[id] = mD.get_space_avail("const", "char", 1)
        return "char"
    else:   
        scope = existsVar(id, currentClass, currentFunct) # call to previous function

        if scope == None:
            raise Exception("Variable '" + id + "' was not declare.")
        else:
            #!!! aquí programar para validar que las variables usadas en expresiones sí estén inicializadas
            return direcClasses[currentClass].c_funcs[scope].f_vars[id].v_type

# ---------------------- END CHECKING VARIABLES EXIST ---------------------- #

# ---------------------- START EXPRESSION SOLVING ---------------------- #

# Function that recieves the operand and adds it and his type in their corresponding stacks
def pushOperand(op):
    global operandsStack
    operandsStack.append(op)
    typesStack.append(getVarType(op))

# Function that recieves a name of an object and the object attribute
# to add it as an operand
def pushObjVar(objName, objAttr):
    global operandsStack, objVarsMemRef, typesStack

    scopeVar = existsVar(objName, currentClass, currentFunct)

    # If object exist then gets the memory of the variable and the class
    if scopeVar != None:
        operandsStack.append("OBJVAR")
        
        classVar = direcClasses[currentClass].c_funcs[scopeVar].f_vars[objName]
        classType = classVar.v_type
        memRefClassType = classVar.memRef

        varType = direcClasses[classType].c_funcs["vG"].f_vars[objAttr]
        typeOfVar = varType.v_type
        memRefOfVar = varType.memRef
        
        typesStack.append(typeOfVar)

        # Concatenate both addresses with a /
        memRefObjVar = str(memRefClassType) + "/" + str(memRefOfVar)
        # Added it to the stack of objects
        objVarsMemRef.append(memRefObjVar)

    else:
        raise Exception("Variable '" + objName + "' was not declare.")

# Function that receives the operator and add it to the operatorsStack
def pushOperator(op):
    global operatorsStack, typesStack, quadList
    operatorsStack.append(op)

# Function to validate and create a quadruaple of logical operators
def pop_op_lop():
    global operatorsStack

    # First we check that the stack isn´t empty
    if operatorsStack and (operatorsStack[-1] == "or" or operatorsStack[-1] == "and"):
        generateExpQuad()

# Function to validate and create a quadruaple of relational operators
def pop_op_relop():
    generateExpQuad()

# Function to pop from our OperatorsStack our fake background when found "("
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
    global operatorsStack, operandsStack, quadList, quadMEM, countOfTemps, quadCounter, typesStack, directConstants
   
    rightOp = operandsStack.pop()
    rightOpType = typesStack.pop()
    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    operator = operatorsStack.pop()

    # Get the matching compatibility of both operands types
    operandsMatch = isAMatch(leftOpType, operator, rightOpType) 
    
    # If operands types are compatible, generate quadruple and update quadcounter, else, throw exception
    if operandsMatch != "error":

        result = "TEMP" + str(countOfTemps)
        # Create the memory reference (Memref) for the temp
        tempResult = mD.get_space_avail("temp", operandsMatch, 1)
        directTemp[result] = tempResult

        # Get the memory reference of the operands
        memRefLeftOp = getVarMemRef(leftOp)
        memRefRightOp = getVarMemRef(rightOp)

        countOfTemps += 1
        quadCounter += 1

        quadList.append(Quadruple(operator, leftOp, rightOp, result))
        quadMEM.append(Quadruple(direcOperators[operator], memRefLeftOp, memRefRightOp, tempResult))

        # Add to the stack the result of the expression
        operandsStack.append(result)
        typesStack.append(operandsMatch)
    
    else:
        raise Exception("Type mismatch")

# ---------------------- END EXPRESSION SOLVING ---------------------- #

# ---------------------- START LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# Function to generate que assignation and add it to the quadList
def pop_op_assign():
    global operatorsStack, operandsStack, quadList, quadCounter, quadMEM
    
    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    varToAssign = operandsStack.pop()
    assignationType = typesStack.pop()
    operator = operatorsStack.pop()   

    # Get the memory reference of the operands
    memRefLeftOp = getVarMemRef(leftOp)
    memVarToAsign = getVarMemRef(varToAssign)
    
    # Validate that the type of the exp result is the same of the variable to assign
    if assignationType == leftOpType:

        # Eliminate the single quotes of the char
        if leftOpType == "char":
            leftOp = leftOp.replace("'", '')

        quadCounter += 1
        quadList.append(Quadruple(operator, leftOp, None, varToAssign))
        quadMEM.append(Quadruple(direcOperators[operator], memRefLeftOp, None, memVarToAsign))

    else:
        raise Exception("Cannot assign variable of type %s with %s" % (assignationType, leftOpType))

# Function that recieves the string to write and saves it
def saveString(s):
    global stringToWrite
    stringToWrite = s

# Function that generates the write quad
def generateWrite():
    global operandsStack, quadList, stringToWrite, quadCounter, typeStack, quadMEM

    # If there is a string to write gets it from helper 
    if (stringToWrite != None):

        varToWrite = stringToWrite
        # Eliminate the double quote of the string
        varToWrite = varToWrite.replace('"', '')

        # Added to the dictionary of constants
        if varToWrite not in directConstants:
            directConstants[varToWrite] = mD.get_space_avail("const", "string", 1)

        # Get the memory reference of the variable
        memVarToWrite = getVarMemRef(varToWrite)
        
        stringToWrite = None # Return the global helper to none

    # Or if it is an expression gets it from the operands stack
    else:
        varToWrite = operandsStack.pop()
        memVarToWrite = getVarMemRef(varToWrite) # Get the memory reference of the variable

        typesStack.pop()

    quadCounter += 1
    quadList.append(Quadruple("WRITE", None, None, varToWrite))
    quadMEM.append(Quadruple(direcOperators["WRITE"], None, None, memVarToWrite))

# Function that generates the read quad
def generateRead():
    global operandsStack, quadList, quadCounter, typesStack, quadMEM

    varToRead = operandsStack.pop()
    memVarToRead = getVarMemRef(varToRead) # Get the memory reference of the variable

    typesStack.pop()
    
    quadCounter += 1
    quadList.append(Quadruple("READ", None, None, varToRead))
    quadMEM.append(Quadruple(direcOperators["READ"], None, None, memVarToRead))

# ---------------------- END LINEAR STATEMENTS (ASSIGN, WRITE, READ) ---------------------- #

# ---------------------- START NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# --- IF --- #

# Function that generates the if GOTOF quad 
# only if the there is a match type otherwise raise exception 
def ifCondition():
    global quadCounter, jumpsStack, typesStack, expType

    expType = typesStack.pop()

    if (expType != "bool"):
        raise Exception("Type mismatch")
    else:
        leftOp = operandsStack.pop()
        memLeftOp = getMemoryRef(leftOp, currentClass, currentFunct) # Get the memory reference of the variable

        quadCounter += 1
        quadList.append(Quadruple("GOTOF", leftOp, None, None))
        quadMEM.append(Quadruple(direcOperators["GOTOF"], memLeftOp, None, None))

        # Add the quadCounter to jump stack to fill later
        jumpsStack.append(quadCounter-1)

# Function that generates the if GOTO quad 
# only if there is an elif condition 
def elifExpression():
    global quadElifExpression, quadCounter, quadMEM, quadList

    quadCounter += 1 
    quadList.append(Quadruple("GOTO", None, None, None))
    quadMEM.append(Quadruple(direcOperators["GOTO"], None, None, None))
    quadElifExpression = quadCounter

    # Add the quadCounter to goto stack to fill later
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
        memLeftOp = getMemoryRef(leftOp, currentClass, currentFunct) # Get the memory reference of the variable

        quadCounter += 1 
        quadList.append(Quadruple("GOTOF", leftOp, None, None))
        quadMEM.append(Quadruple(direcOperators["GOTOF"], memLeftOp, None, None))
        
        # Fill the GOTOF that were before
        quadElif = jumpsStack.pop()
        quadList[quadElif].tResult = quadElifExpression
        quadMEM[quadElif].tResult = quadElifExpression

        # Add the quadCounter to jump stack to fill later
        jumpsStack.append(quadCounter-1)

# Function that generates the else GOTO quad 
def elseCondition():
    global quadCounter, jumpsStack, quadList, quadMEM

    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, None))
    quadMEM.append(Quadruple(direcOperators["GOTO"], None, None, None))
    
    # Fill the GOTOF that were before
    quadElse = jumpsStack.pop()
    quadList[quadElse].tResult = quadCounter
    quadMEM[quadElse].tResult = quadCounter

    # Add the quadCounter to jump stack to fill later
    jumpsStack.append(quadCounter-1)

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
        memExpResult = getMemoryRef(expResult, currentClass, currentFunct) # Get the memory reference of the variable

        quadCounter += 1
        quadList.append(Quadruple("GOTOF", expResult, None, None))
        quadMEM.append(Quadruple(direcOperators["GOTOF"], memExpResult, None, None))

        # Add the quadCounter to jump stack to fill later
        jumpsStack.append(quadCounter - 1)

# Function that generates the while GOTO quad 
# to return to the expression and check it again (cycle)
def endWhile():
    global quadCounter, typesStack, quadList, operandsStack, jumpsStack, quadMEM

    endWhile = jumpsStack.pop()
    whileReturnQuad = jumpsStack.pop()

    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, whileReturnQuad))
    quadMEM.append(Quadruple(direcOperators["GOTO"], None, None, whileReturnQuad))
    
    # Fill the GOTOF that were before
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
        memLeftOp = getMemoryRef(leftOp, currentClass, currentFunct) # Get the memory reference of the variable

        quadCounter += 1
        quadList.append(Quadruple("GOTOF", leftOp, None, None))
        quadMEM.append(Quadruple(direcOperators["GOTOF"], memLeftOp, None, None))

        # Add the quadCounter to jump stack to fill later
        jumpsStack.append(quadCounter-1)

# Function that generates the for GOTO quad 
# to return to the expression and check it again (cycle)
def endFor():
    global quadCounter, jumpsStack, quadList, gotoStack, quadMEM
    
    quadEnd = jumpsStack.pop()
    returnFor = jumpsStack.pop()

    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, returnFor))
    quadMEM.append(Quadruple(direcOperators["GOTO"], None, None, returnFor))

    # Fill the GOTOF that were before
    quadList[quadEnd].tResult = quadCounter
    quadMEM[quadEnd].tResult = quadCounter

# --- END FOR --- #

# ---------------------- END NON-LINEAR STATEMENTS (IF, WHILE, FOR) ---------------------- #

# ---------------------- START FUNCTIONS ---------------------- #

# Function that saves the quadruple where the code of the function starts
def startFunction():
    global currentClass, currentFunct, direcClasses

    direcClasses[currentClass].c_funcs[currentFunct].f_start_quadruple = quadCounter

# Function that saves how many parameters the function has
def insertParams():
    global numberOfParams, currentClass, currentFunct, direcClasses

    direcClasses[currentClass].c_funcs[currentFunct].f_number_params = numberOfParams
    numberOfParams = 0

# Function that creates the quadruple for the return
def returnFunction(variableToReturn):
    global quadCounter, quadList, quadMEM

    functWhereVarExists = existsVar(variableToReturn, currentClass, currentFunct)
    cFunct = direcClasses[currentClass].c_funcs[currentFunct]

    # Validates that the function is not a void type
    if cFunct.f_type != "void":

        # Validates the type of the returnable variable is the same as the type of the function
        if direcClasses[currentClass].c_funcs[functWhereVarExists].f_vars[variableToReturn].v_type == cFunct.f_type:
            
            quadCounter += 1

            memVarToReturn = getMemoryRef(variableToReturn, currentClass, currentFunct)
            # Set the global var for the return function that will be updated with the return result
            memVarToReturnCurrentFunct = getMemoryRef(currentFunct, currentClass, currentFunct) 

            quadList.append(Quadruple("RETURN", currentFunct, None, variableToReturn))
            quadMEM.append(Quadruple(direcOperators["RETURN"], memVarToReturnCurrentFunct, None, memVarToReturn))
            
        else:
            raise Exception("Function is expecting " + cFunct.f_type + " and is given a " + cFunct.f_vars[variableToReturn].v_type)
    else:
        raise Exception("Function of type void can't have return")

# Function that indicates where the function end and release the current var table
def endFunction():
    global quadCounter, quadList, countOfTemps, quadMEM

    # Validates that the function if is a type different than void then has a return
    if direcClasses[currentClass].c_funcs[currentFunct].f_type != "void" and currentFunct not in direcClasses[currentClass].c_funcs["vG"].f_vars:
        raise Exception("Expected return")
    else:
        quadCounter += 1
        quadList.append(Quadruple("END FUNCTION", None, None, None))
        quadMEM.append(Quadruple(direcOperators["END FUNCTION"], None, None, None))
        countOfTemps = 1
        mD.reset_local_space() # kill all memory of current function

# Function that recieves the name of the function called and verify that exists
# if not, an exception is shown
def existFunction(functionCall):
    global direcClasses, functionToCall
   
    if functionCall not in direcClasses[currentClass].c_funcs:
        raise Exception("Function not found")
    else:
        functionToCall = functionCall

# Function that generates the Activation Record expansion new size for the function to be called
def eraSizeFunction():
    global quadCounter, quadList, functionToCall, quadMEM

    quadCounter += 1
    quadList.append(Quadruple("ERA", None, None, functionToCall))
    quadMEM.append(Quadruple(direcOperators["ERA"], None, None, functionToCall))

# Function that recieves the arguments that will be send to the parameters of the function
def argFunction():
    global quadCounter, quadList, operandsStack, typesStack, functionToCall, numberOfArgs, quadMEM

    numberOfArgs += 1
    argument = operandsStack.pop()
    argumentType = typesStack.pop()
    
    memArgument = getVarMemRef(argument) # Get the memory reference of the argument

    # Checks that the function to be called has parameters
    if len(direcClasses["main"].c_funcs[functionToCall].f_params_type) >= numberOfArgs:
        # Check the parameter type is equal to the argument type 
        if direcClasses["main"].c_funcs[functionToCall].f_params_type[numberOfArgs-1] == argumentType:
            quadCounter += 1
            quadList.append(Quadruple("PARAM", argument, None, numberOfArgs-1))
            quadMEM.append(Quadruple(direcOperators["PARAM"], memArgument, None, direcClasses["main"].c_funcs[functionToCall].f_params_memRefs[numberOfArgs-1]))
        else:
            raise Exception("Type mismatch")
    else:
        # If there are more or less arguments sent than parameters recieving in the function generate exception
        raise Exception("Number of arguments mismatch")

# Function that indicates where the code of the function called starts
def gosubFunction():
    global quadCounter, quadList, functionToCall, numberOfArgs, quadMEM, countOfTemps, operandsStack

    # Get the number of paramets of the function to call
    nP = direcClasses["main"].c_funcs[functionToCall].f_number_params
    
    # Check the number of parameters and arguments match
    if numberOfArgs == nP:

        quadCounter += 1
        # Gets the number of the quadruple where the function starts
        functionStart = direcClasses["main"].c_funcs[functionToCall].f_start_quadruple

        quadList.append(Quadruple("GOSUB", None, None, functionStart))
        quadMEM.append(Quadruple(direcOperators["GOSUB"], None, None, functionStart))

        # If the function isn't a type void then we need to assign the returnable variable
        if direcClasses["main"].c_funcs[functionToCall].f_type != "void":

            quadCounter += 1
            result = "TEMP" + str(countOfTemps)
            countOfTemps += 1
            functType = direcClasses[currentClass].c_funcs["vG"].f_vars[functionToCall].v_type
            quadList.append(Quadruple("=", functionToCall, None, result))

            # Get the space of the temporal
            tempResult = mD.get_space_avail("temp", functType, 1)
            directTemp[result] = tempResult

            # Global var that saves "value" of return function 
            memReturnResult = getMemoryRef(functionToCall, currentClass, currentFunct)

            quadMEM.append(Quadruple(direcOperators["="], memReturnResult, None, tempResult))

            operandsStack.append(result)
            typesStack.append(functType)

        functionToCall = "" 
        numberOfArgs = 0
    else:
        raise Exception("Number of arguments mismatch")

#---------------------- END FUNCTIONS ---------------------- #

#---------------------- START DATA STRUCTURES ---------------------- #

# --- ARRAYS --- #

# Verify that the id is an array and creates a fake bottom
def accessArray():
    global operatorsStack, currentDataLowerLimit, accesArrayStack

    currentDataId = operandsStack.pop()
    accesArrayStack.append(currentDataId)
    typesStack.pop()

    # Check that the variable exists
    scopeOfArray = existsVar(currentDataId, currentClass, currentFunct) 
    # Save in global variable the size of the array
    currentArraySize = int(direcClasses[currentClass].c_funcs[scopeOfArray].f_vars[currentDataId].rows)

    # Check that the variable is an array
    if currentArraySize > 0:
        operatorsStack.append("[")
    else:
        raise Exception("Type mismatch")

# Verify that the index of the array to access is an integer and 
# creates quadruple to check that the position is accesible
def verifyArrayIndex():
    global quadCounter, quadList, operandsStack, typesStack, quadMEM, currentDataLowerLimit, currentDataType

    if operandsStack[-1] == "OBJVAR":
        memTopOperand = objVarsMemRef[-1]
    else:
        memTopOperand = getMemoryRef(operandsStack[-1], currentClass, currentFunct)

    currentDataId = accesArrayStack[-1]
    scopeOfArray = existsVar(currentDataId, currentClass, currentFunct)

    # Saves the size, the memory ref where the array starts and the type of array
    currSize = int(direcClasses[currentClass].c_funcs[scopeOfArray].f_vars[currentDataId].rows)
    currentDataLowerLimit = direcClasses[currentClass].c_funcs[scopeOfArray].f_vars[currentDataId].lowerMemRef
    currentDataType = direcClasses[currentClass].c_funcs[scopeOfArray].f_vars[currentDataId].v_type

    if typesStack[-1] == "int":
        quadCounter += 1
        quadList.append(Quadruple("VERIFY", operandsStack[-1], 0, currSize))
        quadMEM.append(Quadruple(direcOperators["VERIFY"], memTopOperand, 0, currSize))
    else:
        raise Exception(currentDataId + " subscript is not an integer")

# Sum the virtual address to access the correct and wanted index
def endArray():
    global quadCounter, quadList, operandsStack, typesStack, operatorsStack, countOfTemps, quadMEM, currentDataLowerLimit, currentDataType

    accesArrayStack.pop() # Pop the current array, since we are done with it
    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    operandsMatch = isAMatch(leftOpType, "+", "int")
    result = "TEMP" + str(countOfTemps)
    countOfTemps += 1

    if operandsMatch != "error":
        # Get the direction memory of the variables
        memLeftOp = getVarMemRef(leftOp)
        memResult = mD.get_space_avail("temp", currentDataType, 1)
        directTemp[result] = -1 * memResult

        # Add to the dictionary of constants the lower direction memory that represents the index of array
        if currentDataLowerLimit not in directConstants:
                directConstants[currentDataLowerLimit] = mD.get_space_avail("const", "int", 1)

        memCurrArrLowLim = getMemoryRef(currentDataLowerLimit, currentClass, currentFunct)

        quadCounter += 1
        quadList.append(Quadruple("BASEADDRESS", leftOp, currentDataLowerLimit, result))
        quadMEM.append(Quadruple(direcOperators["BASEADDRESS"], memLeftOp, memCurrArrLowLim, -1 * memResult))
        
        operandsStack.append(result)
        typesStack.append(currentDataType)
        operatorsStack.pop()
    else:
        raise Exception("Type mismatch")

# --- END ARRAYS --- #

# --- MATRIX --- #

# Verify that the id is an array and creates a fake bottom
def accessMatrix():
    global operandsStack, typesStack, operatorsStack, currentDataType, quadCounter, quadList, countOfTemps, quadMEM, directTemp

    operatorsStack.pop() # delete fake bottom of first dimension of matrix
    leftOp = operandsStack.pop()
    memLeftOperand = getVarMemRef(leftOp)
    leftOpType = typesStack.pop()
    operandsMatch = isAMatch(leftOpType, "*", "int")
    
    if operandsMatch != "error":

        matrixId = accesArrayStack[-1]
        scopeOfMatrix = existsVar(matrixId, currentClass, currentFunct)

        currentMatrixSize = direcClasses[currentClass].c_funcs[scopeOfMatrix].f_vars[matrixId].cols
        memMatrixSize = getMemoryRef(currentMatrixSize, currentClass, currentFunct)
        result = "TEMP" + str(countOfTemps)
        countOfTemps += 1
        memResult =  mD.get_space_avail("temp", operandsMatch, 1)
        directTemp[result] = memResult

        if int(currentMatrixSize) > 0:
            operatorsStack.append("[")
            quadCounter += 1
            quadList.append(Quadruple("*", leftOp, currentMatrixSize, result))
            quadMEM.append(Quadruple(direcOperators["*"], memLeftOperand, memMatrixSize, memResult))
            operandsStack.append(result)
            typesStack.append(operandsMatch)
        else:
            raise Exception("Type mismatch") 
    else:
            raise Exception("Type mismatch")

# Verify that the index of the array to access is an integer and 
# creates quadruple to check that the position is accesible
def verifyMatrixIndex():
    global quadCounter, quadList, operandsStack, typesStack, accesArrayStack, currentDataLowerLimit, countOfTemps, directTemp, currentDataType

    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    rightOp = operandsStack.pop()
    rightOpType = typesStack.pop()
    operandsMatch = isAMatch(leftOpType, "+", rightOpType)
    memLeftOperand = getVarMemRef(leftOp)
    memRightOperand = getVarMemRef(rightOp)
    currentDataId = accesArrayStack[-1]
    scopeOfMatrix = existsVar(currentDataId, currentClass, currentFunct)

    currSize = int(direcClasses[currentClass].c_funcs[scopeOfMatrix].f_vars[currentDataId].cols)
    currentDataLowerLimit = direcClasses[currentClass].c_funcs[scopeOfMatrix].f_vars[currentDataId].lowerMemRef
    currentDataType = direcClasses[currentClass].c_funcs[scopeOfMatrix].f_vars[currentDataId].v_type

    if leftOpType == "int":
        quadCounter += 1
        quadList.append(Quadruple("VERIFY", leftOp, 0, currSize))
        quadMEM.append(Quadruple(direcOperators["VERIFY"], memLeftOperand, 0, currSize))

        if operandsMatch != "error":

            result = "TEMP" + str(countOfTemps)
            countOfTemps += 1
            memResult =  mD.get_space_avail("temp", operandsMatch, 1)
            directTemp[result] = memResult

            quadCounter += 1
            quadList.append(Quadruple("+", leftOp, rightOp, result))
            quadMEM.append(Quadruple(direcOperators["+"], memLeftOperand, memRightOperand, memResult))
            operandsStack.append(result)
            typesStack.append(operandsMatch)

        else:
            raise Exception("Type mismatch")  
    else:
        raise Exception(currentDataId + " subscript is not an integer")


# Sum the virtual address to acces the correct and wanted index
def endMatrix():
    global quadCounter, quadList, operandsStack, typesStack, operatorsStack, countOfTemps, quadMEM

    accesArrayStack.pop()
    leftOp = operandsStack.pop()
    leftOpType = typesStack.pop()
    operandsMatch = isAMatch(leftOpType, "+", "int")
    result = "TEMP" + str(countOfTemps)
    countOfTemps += 1

    if operandsMatch != "error":

        # Get the direction memory of the variables
        memLeftOp = getVarMemRef(leftOp)
        memResult = mD.get_space_avail("temp", currentDataType, 1)
        directTemp[result] = -1 * memResult

        # Add to the dictionary of constants the lower direction memory that represents the index of array
        if currentDataLowerLimit not in directConstants:
            directConstants[currentDataLowerLimit] = mD.get_space_avail("const", "int", 1)

        memCurrArrLowLim = getMemoryRef(currentDataLowerLimit, currentClass, currentFunct)

        quadCounter += 1
        quadList.append(Quadruple("BASEADDRESS", leftOp, currentDataLowerLimit, result))
        quadMEM.append(Quadruple(direcOperators["BASEADDRESS"], memLeftOp, memCurrArrLowLim, -1 * memResult))
        
        operandsStack.append(result)
        typesStack.append(currentDataType)
        operatorsStack.pop()
    else:
        raise Exception("Type mismatch")

# --- END MATRIX --- #

# ---------------------- END DATA STRUCTURES ---------------------- #

# ---------------------- START CLASSES ---------------------- #

def getVarMemRef(op):
    global objVarsMemRef

    if op == "OBJVAR":
        return objVarsMemRef.pop()
    else:
        return getMemoryRef(op, currentClass, currentFunct)

def existMethod(objName, methodName):
    global currentObject, methodToCall, classToAccess

    scopeVar = existsVar(objName, currentClass, currentFunct)

    if scopeVar != None:
        classVar = direcClasses[currentClass].c_funcs[scopeVar].f_vars[objName].v_type

        if methodName not in direcClasses[classVar].c_funcs:
            raise Exception("Function not found")
        else:
            currentObject = objName
            methodToCall = methodName
            classToAccess = classVar
    else:
        raise Exception("Variable '" + objName + "' was not declare.")

def eraSizeMethod():
    global quadCounter, quadList, quadMEM

    scopeVar = existsVar(currentObject, currentClass, currentFunct)
    memRefObj = direcClasses[currentClass].c_funcs[scopeVar].f_vars[currentObject].memRef

    quadCounter += 1
    quadList.append(Quadruple("ERACM", None, currentObject, methodToCall))
    quadMEM.append(Quadruple(direcOperators["ERACM"], None, memRefObj, methodToCall))

def argMethod():
    global quadCounter, quadList, operandsStack, typesStack, numberOfArgs, quadMEM

    numberOfArgs += 1
    argument = operandsStack.pop()
    argumentType = typesStack.pop()
    
    memArgument = getVarMemRef(argument)

    # Checks that the function to be called has parameters
    if len(direcClasses[classToAccess].c_funcs[methodToCall].f_params_type) >= numberOfArgs:
        # Check the parameter type is equal to the argument type 
        if direcClasses[classToAccess].c_funcs[methodToCall].f_params_type[numberOfArgs-1] == argumentType:

            memObj = getMemoryRef(currentObject, currentClass, currentFunct)
            memParam = direcClasses[classToAccess].c_funcs[methodToCall].f_params_memRefs[numberOfArgs-1]
            memRefParam = str(memObj) + "/" + str(memParam)

            quadCounter += 1
            quadList.append(Quadruple("PARAM", argument, None, numberOfArgs-1))
            quadMEM.append(Quadruple(direcOperators["PARAM"], memArgument, None, memRefParam))

        else:
            raise Exception("Type mismatch")
    else:
        # If there are more arguments sent than parameters recieving in the function generate exception
        raise Exception("Number of arguments mismatch") 

def gosubMethod():
    global quadCounter, quadList, classToAccess, methodToCall, numberOfArgs, quadMEM, countOfTemps, operandsStack, currentObject

    nP = direcClasses[classToAccess].c_funcs[methodToCall].f_number_params
    #operandsStack.pop(); este es intento para que jale el error de parametros
    
    # Check the number of parameters and arguments match
    if numberOfArgs == nP:

        quadCounter += 1
        
        # Gets the number of the quadruple where the method starts
        methodStart = direcClasses[classToAccess].c_funcs[methodToCall].f_start_quadruple

        quadList.append(Quadruple("GOSUBCM", None, None, methodStart))
        quadMEM.append(Quadruple(direcOperators["GOSUBCM"], None, None, methodStart))

        if direcClasses[classToAccess].c_funcs[methodToCall].f_type != "void":

            # Creates cuadruple to assign the returnable function to a temp
            quadCounter += 1
            result = "TEMP" + str(countOfTemps)
            countOfTemps += 1
            methodType = direcClasses[classToAccess].c_funcs["vG"].f_vars[methodToCall].v_type
            quadList.append(Quadruple("=", methodToCall, None, result))
            tempResult = mD.get_space_avail("temp", methodType, 1)
            directTemp[result] = tempResult

            # Global var that saves "value" of return function 
            memReturnResult = getMemoryRef(methodToCall, classToAccess, methodToCall)

            quadMEM.append(Quadruple(direcOperators["="], memReturnResult, None, tempResult))
            operandsStack.append(result)
            typesStack.append(methodType)

        currentObject = ""
        methodToCall = ""
        numberOfArgs = 0
    else:
        raise Exception("Number of arguments mismatch")

# ---------------------- END CLASSES ---------------------- #

# ---------------------- START MAIN ---------------------- #

# Function that generates the quadruple at the start of the program to go to the init function
def checkInit():
    global quadCounter, quadList, jumpsStack, quadMEM
    jumpsStack.append(quadCounter)
    quadCounter += 1
    quadList.append(Quadruple("GOTO", None, None, None))
    quadMEM.append(Quadruple(direcOperators["GOTO"], None, None, None))

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
    quadMEM.append(Quadruple(direcOperators["END PROGRAM"], None, None, None))

#---------------------- MEMORY REFERENCES START ---------------------- #

def getMemoryRef(op, classToCheck, funcToCheck):
    global direcClasses, directConstants, directTemp

    scopeOfOp = ""

    if op in directConstants:
        return directConstants[op]
    elif op in directTemp:
        return directTemp[op]
    else:
        scopeOfOp = existsVar(op, classToCheck, funcToCheck)

    return direcClasses[classToCheck].c_funcs[scopeOfOp].f_vars[op].memRef

#---------------------- MEMORY REFERENCES END ---------------------- #
 
def printQuadruples():
    global quadList
    i = 0
    for quad in quadList:
        print("Quad ", i, " symbol: ", quad.operation, " left: ", quad.left_op, " right: ", quad.right_op, " temp: ", quad.tResult)
        i += 1

def printMemoryQuadruples():
    global quadMEM
    i = 0
    for quad in quadMEM:
        print("Quad ", i, " symbol: ", quad.operation, " left: ", quad.left_op, " right: ", quad.right_op, " temp: ", quad.tResult)
        i += 1
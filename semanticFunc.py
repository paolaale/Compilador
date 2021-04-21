# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 16/04/2021

from Classes import Classes
from Functions import Functions
from Vars import Vars

from collections import deque


# stacks to solve expressions
operatorsStack = deque()
operandsStack = deque()
typesStack = deque()

#Queue of quadruples
quadQueue = deque()

direc_classes = {} # dictionary of classes
currentClass = ""
currentFunct = ""
lastVarType = ""

# Match type structure where the key is a hashcode of the types
# and the values is an array where index 0 = OA, index 1 = OR, 
# index 2 = OL
typeMatching = {
    'iinntt': ["int", "bool", "error"],
    'afilnott': ["float", "bool", "error"],
    'achinrt': ["error", "error", "error"],
    'aafflloott': ["float", "bool", "error"],
    'aacfhlort': ["error", "error", "error"],
    'aacchhrr': ["error", "bool", "error"],
    'bblloooo': ["error", "error", "bool"]
}

oA = {"+", "-", "*", "/"}
oR = {"<", ">", "<=", ">=", "==", "!="}
oL = {"and", "or"}


# -------- START ADDING ELEMENTS (FUNCT, CLASSES, VARS) -------- 
# function that recieves the name of class, 
# a boolean that represents if is inherit 
# and the name of the parent if is inherit, otherwise recieve None
def addClass(cName, cInherits, cParentName):
    global direc_classes, currentClass, currentFunct
    currentClass = cName 
    currentFunct = ""
    # add to the dictionary of classes the class
    direc_classes[cName] = Classes(cInherits, cParentName) 

# function that recieves the name of the function 
# and the type of return
def addFunction(fName, fType):
    global currentClass, currentFunct
    currentFunct = fName
    # add to dictionary of classes, in the current class the function
    direc_classes[currentClass].c_funcs[fName] = Functions(fType) 

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
        direc_classes[currentClass].c_funcs[currentFunct].f_vars[vName] = Vars(vType, vSize1, vSize2)
    else:
        # add to dictionary of classes, in the current class and global variables "fucntion" the variables
        direc_classes[currentClass].c_funcs["vG"].f_vars[vName] = Vars(vType, vSize1, vSize2)

# -------- END ADDING ELEMENTS (FUNCT, CLASSES, VARS) -------- 
    
# -------- START CHECKING MATCH TYPES -------- 

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
    #print("resultado: ", resultType)

# -------- END CHECKING MATCH TYPES -------- 

# verify that a variable exists
def getVarType(id):
    global currentFunct, currentClass
    scope = existsVar(id)

    if scope == None:
        print("Deberíamos retornear o arrojar error porque no existe la variable")
        return "no existe"
    else:
        print(direc_classes[currentClass].c_funcs[scope].f_vars[id].v_type)
        return direc_classes[currentClass].c_funcs[scope].f_vars[id].v_type
        

def existsVar(id):
    global currentFunct, currentClass

    funcs = direc_classes[currentClass].c_funcs

    if id in funcs[currentFunct].f_vars:
        return currentFunct
    elif id in funcs["vG"].f_vars:
        return "vG"
    else:
        return None

# -------- START EXPRESSION SOLVING -------- 

def pushOperand(op):
    global operandsStack
    operandsStack.append(op)

# -------- END EXPRESSION SOLVING -------- 
# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 16/04/2021

from Classes import Classes
from Functions import Functions
from Vars import Vars

direc_classes = {} # dictionary of classes
currentClass = ""
currentFunct = ""
lastVarType = ""

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

    


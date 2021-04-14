from symbolTables import Functions

direc_functions = {}
global_vars = {}
lastVarType = ""

def addVars(vName, vType):
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType
    #print("last var = ", lastVarType)
    print(vName, "-", vType)

def addArrayVar(vName, vType, vSize):
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType
    print(vName, "-", vType, "-", vSize)

def addMatrixVar(vName, vType, vSize1, vSize2):
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType
    print(vName, "-", vType, "-", vSize1, "-", vSize2)

def addFunction(fName, fType):
    f = Functions(fType)
    direc_functions[fName] = f
    #print(direc_functions[fName].f_type)


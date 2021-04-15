from symbolTables import Functions, Vars

direc_functions = {"vG": Functions("global")}
global_vars = {}
lastVarType = ""
currentFunct = "";

def addVars(vName, vType, vSize1, vSize2):
    global lastVarType, direc_functions, currentFunct
    if (vType == ','):
        vType = lastVarType
    else:
        lastVarType = vType

    if currentFunct != "":
        direc_functions[currentFunct].f_vars[vName] = Vars(vType, vSize1, vSize2)
    else:
        direc_functions["vG"].f_vars[vName] = Vars(vType, vSize1, vSize2)

def addFunction(fName, fType):
    global direc_functions, currentFunct
    currentFunct = fName
    direc_functions[fName] = Functions(fType)
    


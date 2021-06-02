# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 28/05/2021

import semanticFunc as sF
from collections import deque
from MemoryAllocator import MemoryAllocator
from copy import copy

# Stack that keeps order of the contexts/scopes executions
exeStack = deque()
# Stack that keeps the current global memory context and the order to be executed
objMemoryInFuncsStack = deque() 
# Variable to access the corresponding global memory, initialize it with the memory of the main class
currentGlobalMemory = 0
# Variable to keep the past Obj memory and know in which context the variables need to be used
previousObjInstanceMemory = 0
currentLocalMemory = ""

# Dictionary of global memories with the main class memory
globalMemories = dict()
globalMemories[0] = MemoryAllocator()

# First local memory to be used
initMemory = MemoryAllocator()
# Creation of the dictionary of constants
constDictionary = dict()

# Stack to do the correct jumps in the quadruples when using functions calls 
exeGoSubStack = deque()

# Flaf that helps to know if an expression is in function with parameters context
paramExpression = False

# Save here the previous memory when passing args to a function
previousMemory = MemoryAllocator()

#---------------------- FUNCTIONS FOR QUADRUPLES ---------------------- #

# Function to initialize all global memories that require a first value or modification before reading the quadruples
def dataInit():
    global constDictionary, objMemoryInFuncsStack, exeStack, initMemory

    constDictionary = dict((value, key) for key, value in sF.directConstants.items()) # set the dictionary of constants with all the ones found in compilation
    exeStack.append(initMemory) # Add first memory to be used, that is the one for init method of the main class
    objMemoryInFuncsStack.append(0) # Set firt global memory that is being used
    addGlobalObjInstances() # Initialize all memories for global objects

# Function to initialize all global memories with all the global objects found in compilation
def addGlobalObjInstances():
    global globalMemories

    i = 0
    for instance in sF.directObjInstances:
        globalMemories[instance] = MemoryAllocator();
        i += 1

# Function to verify that the code doesn´t generate and StackOverFlowError
def checkStackMemory():
    global exeStack

    if len(exeStack) > 2500:
        raise Exception("Exception: StackOverFlowError")

def getCorrectMemRef(memRef, stackToCheck):
    memRefString = str(memRef)
  
    if "/" in memRefString:
        
        return memRef

    if memRef >= 0:
        return memRef

    if stackToCheck == "previous":
        if memRef not in previousMemory.vars:
            return memRef
        else:
            return previousMemory.vars[memRef]
    elif stackToCheck == "current":
        if memRef not in exeStack[-1].vars:
            return memRef
        else:
            return exeStack[-1].vars[memRef]

#!!!! aquí programar para validar que las variables usadas en expresiones sí estén inicializadas
def getValue(memRef):
    global constDictionary, currentGlobalMemory
    
    auxCurrentGlobalMemory = currentGlobalMemory # To preserve the currGlobalMem if we need to access the memory of an obj
    memRefString = str(memRef) # We convert to string the Memref
   
    # We check if the memRef belongs to an instance of an object and then access to its value
    if "/" in memRefString:
       
        objMemoryInfo = memRefString.split("/")
        objInstanceMemory = objMemoryInfo[0]
        objAttrMemory = objMemoryInfo[1]
        
        currentGlobalMemory = int(objInstanceMemory)
        memRef = int(objAttrMemory)

    if memRef in constDictionary:
        if memRef < 36000:
            return int(constDictionary[memRef])
        elif memRef < 37000:
            return float(constDictionary[memRef])
        else:
            return constDictionary[memRef] #!!!! falta lógica de chars aquí
        
    elif memRef in exeStack[-1].vars:
        return exeStack[-1].vars[memRef]
    else:
        
        memRefToReturn = globalMemories[currentGlobalMemory].vars[memRef]
        currentGlobalMemory = auxCurrentGlobalMemory

        return memRefToReturn

def assignValue(val1, container):
    global exeStack, globalMemories, currentGlobalMemory

    auxCurrentGlobalMemory = currentGlobalMemory
    memRefString = str(container)

    if "/" in memRefString:
        objMemoryInfo = memRefString.split("/")
        objInstanceMemory = objMemoryInfo[0]
        objAttrMemory = objMemoryInfo[1]

        currentGlobalMemory = int(objInstanceMemory)
        container = int(objAttrMemory)
    
    valToAsign = getValue(val1)
     
    if (container >= 0 and container < 4000) or (container >= 5000 and container < 8999): 
        globalMemories[currentGlobalMemory].vars[container] = valToAsign
    else:
        exeStack[-1].vars[container] = valToAsign
    currentGlobalMemory = auxCurrentGlobalMemory

def assignReadValue(container, newValue):
    global exeStack, globalMemories, currentGlobalMemory

    auxCurrentGlobalMemory = currentGlobalMemory
    memRefString = str(container)

    if "/" in memRefString:
        objMemoryInfo = memRefString.split("/")
        objInstanceMemory = objMemoryInfo[0]
        objAttrMemory = objMemoryInfo[1]

        currentGlobalMemory = int(objInstanceMemory)
        container = int(objAttrMemory)

    if (container >= 0 and container < 4000) or (container >= 5000 and container < 8999):
        globalMemories[currentGlobalMemory].vars[container] = newValue
    else:
        exeStack[-1].vars[container] = newValue

    currentGlobalMemory = auxCurrentGlobalMemory

def readValue(container):

    memRefString = str(container)
    varOfObject = False

    if "/" in memRefString:
        varOfObject = True;
        objMemoryInfo = memRefString.split("/")
        objAttrMemory = objMemoryInfo[1]
        auxContainer = container
        container = int(objAttrMemory)
    
    if (container >= 0 and container < 4000) or (container >= 17000 and container < 22000):
        newValue = int(input())
    elif (container >= 5000 and container < 8999) or (container >= 23000 and container < 27999):
        newValue = float(input())
    else:
        newValue = input() 
        if len(newValue) != 1:
            raise Exception("Cannot assign string to a char")

    if varOfObject:
        container = auxContainer;

    assignReadValue(container, newValue)

def getParamValue(memRef):
    global constDictionary, previousMemory, globalMemories, currentGlobalMemory

    auxCurrentGlobalMemory = currentGlobalMemory # To preserve the currGlobalMem if we need to access the memory of an obj
    memRefString = str(memRef) # We convert to string the Memref
   
    # We check if the memRef belongs to an instance of an object and then access to its value
    if "/" in memRefString:
       
        objMemoryInfo = memRefString.split("/")
        objInstanceMemory = objMemoryInfo[0]
        objAttrMemory = objMemoryInfo[1]
        
        currentGlobalMemory = int(objInstanceMemory)
        memRef = int(objAttrMemory)
    
    if memRef in constDictionary:
        if memRef < 36000:
            return int(constDictionary[memRef])
        elif memRef < 37000:
            return float(constDictionary[memRef])
        else:
            return constDictionary[memRef] #!!!! falta lógica de chars aquí
    elif memRef in previousMemory.vars:
        return previousMemory.vars[memRef]
    else:
        memRefToReturn = globalMemories[currentGlobalMemory].vars[memRef]
        currentGlobalMemory = auxCurrentGlobalMemory

        return memRefToReturn

# Assign argument of a function call to the parameter
def assignParameter(val1, container):
    memRefString = str(container) # We convert to string the Memref
   
    # We check if the memRef belongs to an instance of an object and then access to its value
    if "/" in memRefString:
       
        objMemoryInfo = memRefString.split("/")
        objAttrMemory = objMemoryInfo[1]
        container = int(objAttrMemory)
        
    valToAsign = getParamValue(val1)

    exeStack[-1].vars[container] = valToAsign
   

#---------------------- END FUNCTIONS FOR QUADRUPLES ---------------------- #

#---------------------- EXECUTE ---------------------- #

def execute(quadList):
    global exeStack, globalMemories, exeGoSubStack, previousMemory, paramExpression, memRefGoSub, currentGlobalMemory, objMemoryInFuncsStack, previousObjInstanceMemory
    
    dataInit()
    print(constDictionary)
    i = 0

    while True:
        
        checkStackMemory()

        if quadList[i].operation == 1:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) + getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) + getValue(getCorrectMemRef(quadList[i].right_op, "current"))
            #print("SUMA")

        elif quadList[i].operation == 2:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) - getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) - getValue(getCorrectMemRef(quadList[i].right_op, "current"))
            #print("RESTA")

        elif quadList[i].operation == 3:
            #print("START OF MULTIPLICATION", quadList[i].left_op);
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) * getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) * getValue(getCorrectMemRef(quadList[i].right_op, "current"))
            #print("MULTIPLICACIÓN")

        elif quadList[i].operation == 4:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) / getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) / getValue(getCorrectMemRef(quadList[i].right_op, "current"))
            #print("DIVISION")

        elif quadList[i].operation == 5:
            if paramExpression:
                left_op = getCorrectMemRef(quadList[i].left_op, "previous")
                tResult = getCorrectMemRef(quadList[i].tResult, "previous")
            else:
                left_op = getCorrectMemRef(quadList[i].left_op, "current")
                tResult = getCorrectMemRef(quadList[i].tResult, "current")
            
            assignValue(left_op, tResult)
            #print("ASSIGN")

        elif quadList[i].operation == 6:
            if getValue(quadList[i].left_op) and getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("AND")

        elif quadList[i].operation == 7:
            if getValue(quadList[i].left_op) or getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("OR")

        elif quadList[i].operation == 8:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) > getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("MAYOR QUE")

        elif quadList[i].operation == 10:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) < getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("MENOR QUE")
            
        elif quadList[i].operation == 9:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) >= getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("MAYOR O IGUAL QUE")

        elif quadList[i].operation == 11:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) <= getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("MENOR O IGUAL QUE")

        elif quadList[i].operation == 12:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) == getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("IGUAL QUE")

        elif quadList[i].operation == 13:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) != getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            #print("DIFERENTE QUE")

        elif quadList[i].operation == 15:
            print("WRITE: ", getValue(getCorrectMemRef(quadList[i].tResult, "current")))

        elif quadList[i].operation == 16:
            print("insert value: ")
            readValue(getCorrectMemRef(quadList[i].tResult, "current"))
            #print("READ")

        elif quadList[i].operation == 17:
            i = quadList[i].tResult - 1
            #print("GOTO")

        elif quadList[i].operation == 18:
            if getValue(quadList[i].left_op) == False:
                i = quadList[i].tResult - 1
            #print("GOTOF")

        elif quadList[i].operation == 19:
            previousMemory = copy(exeStack[-1])
            paramExpression = True
            exeStack.append(MemoryAllocator())
            #print("ERA")

        elif quadList[i].operation == 20:
            
            assignParameter(getCorrectMemRef(quadList[i].left_op, "previous"), quadList[i].tResult)
            #print("PARAM")

        elif quadList[i].operation == 21:
            paramExpression = False
            exeGoSubStack.append(i) # we save where to jump back
            i = quadList[i].tResult - 1
            #print("GOSUB")

        elif quadList[i].operation == 14:
            #print("verify memref: ", quadList[i].left_op);
            if paramExpression:
                index = getValue(getCorrectMemRef(quadList[i].left_op, "previous"))
            else:
                index = getValue(getCorrectMemRef(quadList[i].left_op, "current"))
        
            if not(index >= 0 and index < quadList[i].tResult):
                raise Exception("Array index out of bounds exception", index)
            #print("VERIFY")

        elif quadList[i].operation == 22:
            globalMemories[currentGlobalMemory].vars[quadList[i].left_op] =  getValue(quadList[i].tResult)
            #print("RETURN")

        elif quadList[i].operation == 23:
            exeStack.pop()
            i = exeGoSubStack.pop()
            #currentGlobalMemory = 0 # we reset to the AQUII UNA STAAACK
            
            if currentGlobalMemory != previousObjInstanceMemory:
                objMemoryInFuncsStack.pop()
                currentGlobalMemory = objMemoryInFuncsStack[-1]
            #print("END FUNCTION")

        elif quadList[i].operation == 24:
            if paramExpression:
                previousMemory.vars[quadList[i].tResult] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) + getParamValue(quadList[i].right_op)
                #previousMemory.vars[previousMemory.vars[quadList[i].tResult]] = -1;
            else:
                exeStack[-1].vars[quadList[i].tResult] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) + getValue(quadList[i].right_op)
                #exeStack[-1].vars[exeStack[-1].vars[quadList[i].tResult]] = -1;
            #print("BASEADDRESS")

        # Create the memory for an object instance when found "ERAC" in quadruple
        elif quadList[i].operation == 25:
            globalMemories[quadList[i].tResult] = MemoryAllocator()
            #print("ERAC")
        
        # Add the memory to use for the function call of an object and set the currentGlobalMemory to use the correct global context
        elif quadList[i].operation == 26:
            previousMemory = copy(exeStack[-1])
            paramExpression = True
            exeStack.append(MemoryAllocator())
            # to know in which memory the function to call needs to be executed
            previousObjInstanceMemory = objMemoryInFuncsStack[-1]
            objMemoryInFuncsStack.append(quadList[i].right_op)

            #print("ERACM", memRefGoSub)

        elif quadList[i].operation == 27:
            paramExpression = False # we reset the context to know the parameters assignation ended
            exeGoSubStack.append(i) # we save where to jump back
            i = quadList[i].tResult - 1 # We set the index iterator to the quad to jump
            #currentGlobalMemory = memRefGoSub
            currentGlobalMemory = objMemoryInFuncsStack[-1]
            #print("GOSUBCM", currentGlobalMemory)
            
        elif quadList[i].operation == 28:
            print("Direct Local: ", exeStack[-1].vars)
            print("Direct global: ", globalMemories[currentGlobalMemory].vars)
            print("GlobalMemories: ", globalMemories)
            print("FINALCURGLMEMORY", currentGlobalMemory)
            print("length of Dictionary ", len(globalMemories))
           

            print("END PROGRAM")
            break

        else:
            print("ERROR")

        i += 1
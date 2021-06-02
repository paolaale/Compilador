# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 02/06/2021

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
        globalMemories[instance] = MemoryAllocator()
        i += 1

# Function to verify that the code doesn´t generate and StackOverFlowError
def checkStackMemory():
    global exeStack

    if len(exeStack) > 2500:
        raise Exception("Exception: StackOverFlowError")

# Function to detect the location or type of Memory Reference that needs to be used
def getCorrectMemRef(memRef, stackToCheck):
    memRefString = str(memRef)
  
    # Check if we need the memory of an attribute of an object
    if "/" in memRefString:
        return memRef

    # Check if the memory is not from an array or matrix
    if memRef >= 0:
        return memRef

    # Check location of the memory reference of an array or matrix
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

# Function to obtain the real value of a variable through its memory reference
def getValue(memRef):
    global constDictionary, currentGlobalMemory
    
    auxCurrentGlobalMemory = currentGlobalMemory # To preserve the currGlobalMem if we need to access the memory of an obj
    memRefString = str(memRef) # We convert to string the Memref
   
    # We check if the memRef belongs to an instance of an object and then access to its value
    if "/" in memRefString:
       
        objMemoryInfo = memRefString.split("/") # Split the memRef of the object to obtain the memories
        objInstanceMemory = objMemoryInfo[0] # Save global memory to enter for this variable
        objAttrMemory = objMemoryInfo[1] # Save the memory ref of the attribute of the object
        
        currentGlobalMemory = int(objInstanceMemory) # Update global memory to the one of the object to access
        memRef = int(objAttrMemory) # Save memory ref of the attribute in the correct format (int)

    # Check if the memory ref of a variables belongs to a constants memory range
    if memRef in constDictionary: 
        # Memory ref is an int
        if memRef < 36000:
            return int(constDictionary[memRef])
        # Memory ref is a float
        elif memRef < 37000:
            return float(constDictionary[memRef])
        # Memory ref is a char
        else:
            return constDictionary[memRef]
    # Check if memory ref of variable is local (exists in the current funct memory)
    elif memRef in exeStack[-1].vars:
        return exeStack[-1].vars[memRef]
    # The memory ref of the variable exists in the global memory
    else:
        try:
            memRefToReturn = globalMemories[currentGlobalMemory].vars[memRef]
        except:
            raise Exception("Variable has not been initialized")
        currentGlobalMemory = auxCurrentGlobalMemory

        return memRefToReturn

# Function to assign the value of a variable to other through their memories refs
def assignValue(val1, container):
    global exeStack, globalMemories, currentGlobalMemory

    # Save currrent global memory in case one of the operands in the assignation exist in other global memory
    # for example, in an instance of an object
    auxCurrentGlobalMemory = currentGlobalMemory
    memRefString = str(container) # Convert/Normalize the mem ref of the container to a string

    # Check if the container memory ref belongs to an object instance
    if "/" in memRefString:
        objMemoryInfo = memRefString.split("/")
        objInstanceMemory = objMemoryInfo[0]
        objAttrMemory = objMemoryInfo[1]

        currentGlobalMemory = int(objInstanceMemory)
        container = int(objAttrMemory)
    
    # Obtains the value to be assigned in the container
    valToAsign = getValue(val1)
     
    # Check if the container is a global memory through its range or if it is local
    if (container >= 0 and container < 4000) or (container >= 5000 and container < 9000) or (container >= 10000 and container < 13000): 
        globalMemories[currentGlobalMemory].vars[container] = valToAsign
    else:
        exeStack[-1].vars[container] = valToAsign

    currentGlobalMemory = auxCurrentGlobalMemory # Revert the currentGlobalMemory

# Function to assign the value of a variable to other through their memories refs when using a read() (scanner) in the program
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

    # Check if the container is a global memory through its range or if it is local
    if (container >= 0 and container < 4000) or (container >= 5000 and container < 9000) or (container >= 10000 and container < 13000):
        globalMemories[currentGlobalMemory].vars[container] = newValue
    else:
        exeStack[-1].vars[container] = newValue

    currentGlobalMemory = auxCurrentGlobalMemory

# Function to read the correct type of variable that the users want
def readValue(container):

    memRefString = str(container)
    varOfObject = False

    if "/" in memRefString:
        varOfObject = True # Set that the variable to read belongs to an object
        objMemoryInfo = memRefString.split("/")
        objAttrMemory = objMemoryInfo[1]
        auxContainer = container
        container = int(objAttrMemory)
    
    # Container needs to save an int
    if (container >= 0 and container < 4000) or (container >= 17000 and container < 22000):
        newValue = int(input())
    # Container needs to save a float
    elif (container >= 5000 and container < 8999) or (container >= 23000 and container < 27999):
        newValue = float(input())
    # Container needs to save an char
    else:
        newValue = input() 
        if len(newValue) != 1:
            raise Exception("Cannot assign string to a char")

    # If we read an attribute of an object, revert the container to its original
    if varOfObject:
        container = auxContainer;

    # Send to function the memory ref of the container and the value to be holded
    assignReadValue(container, newValue)

# Function to get the correct memory reference of a parameter to be assigned
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
            return constDictionary[memRef]
    elif memRef in previousMemory.vars:
        return previousMemory.vars[memRef]
    else:
        try:
            memRefToReturn = globalMemories[currentGlobalMemory].vars[memRef]
        except:
            raise Exception("Variable has not been initialized")
        currentGlobalMemory = auxCurrentGlobalMemory

        return memRefToReturn

# Assign argument of a function call to the parameter
def assignParameter(val1, container):
    memRefString = str(container) # Convert to string the Memref
   
    # Check if the memRef belongs to an instance of an object and then access to its value
    if "/" in memRefString:
       
        objMemoryInfo = memRefString.split("/")
        objAttrMemory = objMemoryInfo[1]
        container = int(objAttrMemory)
        
    valToAsign = getParamValue(val1)

    exeStack[-1].vars[container] = valToAsign
   
#---------------------- END FUNCTIONS FOR QUADRUPLES ---------------------- #

#---------------------- EXECUTE ---------------------- #

# Function that reads and execute all the quadruples received from the semantic of the compilation
def execute(quadList):
    global exeStack, globalMemories, exeGoSubStack, previousMemory, paramExpression, memRefGoSub, currentGlobalMemory, objMemoryInFuncsStack, previousObjInstanceMemory

    dataInit() # Initialize the global variables
    i = 0 # Set the iterator to the quadruple 0

    # Iterate quadList until END PROGRAM or Error is reached
    while True:
        
        checkStackMemory() # Check that there is space for calling functions

        # Instruction to sum two variables/values
        if quadList[i].operation == 1:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) + getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) + getValue(getCorrectMemRef(quadList[i].right_op, "current"))

        # Instruction to substract two variables/values
        elif quadList[i].operation == 2:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) - getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) - getValue(getCorrectMemRef(quadList[i].right_op, "current"))

        # Instruction to multiply two variables/values
        elif quadList[i].operation == 3:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) * getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) * getValue(getCorrectMemRef(quadList[i].right_op, "current"))

        # Instruction to divide two variables/values
        elif quadList[i].operation == 4:
            if paramExpression:
                previousMemory.vars[getCorrectMemRef(quadList[i].tResult, "previous")] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) / getParamValue(getCorrectMemRef(quadList[i].right_op, "previous"))
            else:
                exeStack[-1].vars[getCorrectMemRef(quadList[i].tResult, "current")] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) / getValue(getCorrectMemRef(quadList[i].right_op, "current"))
        
        # Instruction to assign a value to a variable
        elif quadList[i].operation == 5:
            if paramExpression:
                left_op = getCorrectMemRef(quadList[i].left_op, "previous")
                tResult = getCorrectMemRef(quadList[i].tResult, "previous")
            else:
                left_op = getCorrectMemRef(quadList[i].left_op, "current")
                tResult = getCorrectMemRef(quadList[i].tResult, "current")
            
            assignValue(left_op, tResult) # Call function to assign value to corresponding variable

        # Instruction to validate logical operation "AND" of two values
        elif quadList[i].operation == 6:
            if getValue(quadList[i].left_op) and getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to validate logical operation "OR" of two values
        elif quadList[i].operation == 7:
            if getValue(quadList[i].left_op) or getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to validate relationar operation ">" of two values
        elif quadList[i].operation == 8:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) > getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to validate relationar operation "<" of two values
        elif quadList[i].operation == 10:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) < getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
        
        # Instruction to validate relationar operation ">=" of two values
        elif quadList[i].operation == 9:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) >= getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to validate relationar operation "<=" of two values
        elif quadList[i].operation == 11:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) <= getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to validate relationar operation "==" of two values
        elif quadList[i].operation == 12:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) == getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to validate relationar operation "!=" of two values
        elif quadList[i].operation == 13:
            if getValue(getCorrectMemRef(quadList[i].left_op, "current")) != getValue(getCorrectMemRef(quadList[i].right_op, "current")):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False

        # Instruction to verify if a position to be accessed in an array or matrix is in the range of its size
        elif quadList[i].operation == 14:
            if paramExpression:
                index = getValue(getCorrectMemRef(quadList[i].left_op, "previous"))
            else:
                index = getValue(getCorrectMemRef(quadList[i].left_op, "current"))
        
            if not(index >= 0 and index < quadList[i].tResult):
                raise Exception("Array index out of bounds exception", index)
        
        # Instruction to print the value of a variable or a constant
        elif quadList[i].operation == 15:
            print(getValue(getCorrectMemRef(quadList[i].tResult, "current")))

        # Instruction to read a constant and assigned it to a variable
        elif quadList[i].operation == 16:
            readValue(getCorrectMemRef(quadList[i].tResult, "current"))

        # Instruction to jump to que corresponding quadruple in que quadlist
        elif quadList[i].operation == 17:
            i = quadList[i].tResult - 1

        # Instruction to jump to que corresponding quadruple in que quadlist
        elif quadList[i].operation == 18:
            if getValue(quadList[i].left_op) == False:
                i = quadList[i].tResult - 1

        # Instruction to append to the exeStack a new memory when a function is called
        elif quadList[i].operation == 19:
            previousMemory = copy(exeStack[-1])
            paramExpression = True
            exeStack.append(MemoryAllocator())

        # Instruction to assign an argument to a parameter
        elif quadList[i].operation == 20:
            assignParameter(getCorrectMemRef(quadList[i].left_op, "previous"), quadList[i].tResult)

        # Instruction to make iterator go to the quadruples where the function called start
        elif quadList[i].operation == 21:
            paramExpression = False
            exeGoSubStack.append(i) # we save where to jump back
            i = quadList[i].tResult - 1

        # Instruction to assign value returned of a function to its corresponding global variable
        elif quadList[i].operation == 22:
            globalMemories[currentGlobalMemory].vars[quadList[i].left_op] =  getValue(quadList[i].tResult)

        # Instruction to indicate that a function call has ended in order to pop its instance memory from exeStack
        elif quadList[i].operation == 23:
            exeStack.pop()
            i = exeGoSubStack.pop()
            
            if currentGlobalMemory != previousObjInstanceMemory:
                objMemoryInFuncsStack.pop()
                currentGlobalMemory = objMemoryInFuncsStack[-1]
        
        # Instruction to sum the positional to be index in an array or matrix to its base memory reference
        elif quadList[i].operation == 24:
            if paramExpression:
                previousMemory.vars[quadList[i].tResult] = getParamValue(getCorrectMemRef(quadList[i].left_op, "previous")) + getParamValue(quadList[i].right_op)
            else:
                exeStack[-1].vars[quadList[i].tResult] = getValue(getCorrectMemRef(quadList[i].left_op, "current")) + getValue(quadList[i].right_op)

        # Instruction to create the memory for an object instance when found "ERAC" in quadruple
        elif quadList[i].operation == 25:
            globalMemories[quadList[i].tResult] = MemoryAllocator()
        
        # Instruction to add the memory to use for the function call of an object and set the currentGlobalMemory to use the correct global context
        elif quadList[i].operation == 26:
            previousMemory = copy(exeStack[-1])
            paramExpression = True
            exeStack.append(MemoryAllocator())
            # to know in which memory the function to call needs to be executed
            previousObjInstanceMemory = objMemoryInFuncsStack[-1]
            objMemoryInFuncsStack.append(quadList[i].right_op)
        
        # Instruction to make iterator go to the quadruples where the function called start when calling an object method
        elif quadList[i].operation == 27:
            paramExpression = False # we reset the context to know the parameters assignation ended
            exeGoSubStack.append(i) # we save where to jump back
            i = quadList[i].tResult - 1 # We set the index iterator to the quad to jump
            currentGlobalMemory = objMemoryInFuncsStack[-1]
        
        # Instruction to indicate that the program has ended and stop the execution of the quadList
        elif quadList[i].operation == 28:
            break

        else:
            print("ERROR")

        i += 1
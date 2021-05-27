# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 21/05/2021

import semanticFunc as sF
from collections import deque
from MemoryAllocator import MemoryAllocator
from copy import copy

exeStack = deque()
executionStack = dict()

currentGlobalMemory = "main"
currentLocalMemory = ""

globalMemories = dict()
globalMemories["main"] = MemoryAllocator()

initMemory = MemoryAllocator()
constDictionary = dict()

exeStack.append(initMemory)
exeGoSubStack = deque()

paramExpression = False

# We save here the previous memory when passing args to a function
previousMemory = MemoryAllocator();
### Functions for quadruples ###
def dataInit():
    global constDictionary
    constDictionary = dict((value, key) for key, value in sF.directConstants.items()) 

def getValue(memRef):
    global constDictionary
    
    if memRef in constDictionary:
        if memRef < 36000:
            return int(constDictionary[memRef])
        elif memRef < 37000:
            return float(constDictionary[memRef])
        else:
            return constDictionary[memRef] #falta lógica de chars aquí
    elif memRef in exeStack[-1].vars:
        return exeStack[-1].vars[memRef]
    else:
        return globalMemories[currentGlobalMemory].vars[memRef]

def assignValue(val1, container):
    global exeStack, globalMemories
    valToAsign = getValue(val1)
     
    if (container >= 0 and container < 4000) or (container >= 5000 and container < 8999):   

        globalMemories[currentGlobalMemory].vars[container] = valToAsign
        
    else:

        exeStack[-1].vars[container] = valToAsign


def assignReadValue(container, newValue):
    if (container >= 0 and container < 4000) or (container >= 5000 and container < 8999):
        globalMemories[currentGlobalMemory].vars[container] = newValue
    else:
        exeStack[-1].vars[container] = newValue

def readValue(container):
    
    if (container >= 0 and container < 4000) or (container >= 17000 and container < 22000):
        newValue = int(input())
    elif (container >= 5000 and container < 8999) or (container >= 23000 and container < 27999):
        newValue = float(input())
    else:
        newValue = input()#aquí falta implementar bien la lógica para los chars

    assignReadValue(container, newValue)

def getParamValue(memRef):
    global constDictionary, previousMemory, globalMemories
    
    if memRef in constDictionary:
        if memRef < 36000:
            return int(constDictionary[memRef])
        elif memRef < 37000:
            return float(constDictionary[memRef])
        else:
            return constDictionary[memRef] #falta lógica de chars aquí
    elif memRef in previousMemory.vars:
        return previousMemory.vars[memRef]
    else:
        return globalMemories[currentGlobalMemory].vars[memRef]

# assign argument of a function call to the parameter
def assignParameter(val1, container):
    print("ASSIGNPARAMETER val1", val1);
    print("ASSIGNPARAMETER container", container);
    valToAsign = getParamValue(val1)
    exeStack[-1].vars[container] = valToAsign



### Read and execute quadruples
def execute(quadList):
    global exeStack, globalMemories, exeGoSubStack, previousMemory, paramExpression
    dataInit()

    i = 0

    while quadList[i].operation != 24:

        if quadList[i].operation == 1:
            if paramExpression:
                previousMemory.vars[quadList[i].tResult] = getParamValue(quadList[i].left_op) + getParamValue(quadList[i].right_op)
            else:
                exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) + getValue(quadList[i].right_op)
            print("SUMA")
        elif quadList[i].operation == 2:
            if paramExpression:
                previousMemory.vars[quadList[i].tResult] = getParamValue(quadList[i].left_op) - getParamValue(quadList[i].right_op)
            else:
                exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) - getValue(quadList[i].right_op)
            print("RESTA")
        elif quadList[i].operation == 3:
            print("START OF MULTIPLICATION", quadList[i].left_op);

            if paramExpression:
                previousMemory.vars[quadList[i].tResult] = getParamValue(quadList[i].left_op) * getParamValue(quadList[i].right_op)
            else:
                exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) * getValue(quadList[i].right_op)
            print("MULTIPLICACIÓN")
        elif quadList[i].operation == 4:
            if paramExpression:
                previousMemory.vars[quadList[i].tResult] = getParamValue(quadList[i].left_op) / getParamValue(quadList[i].right_op)
            else:
                exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) / getValue(quadList[i].right_op)
            print("DIVISION")
        elif quadList[i].operation == 5:
            assignValue(quadList[i].left_op, quadList[i].tResult)
            print("ASSIGN")
        elif quadList[i].operation == 6:
            if getValue(quadList[i].left_op) and getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("AND")
        elif quadList[i].operation == 7:
            if getValue(quadList[i].left_op) or getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("OR")
        elif quadList[i].operation == 8:
            if getValue(quadList[i].left_op) > getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("MAYOR QUE")
        elif quadList[i].operation == 10:
            if getValue(quadList[i].left_op) < getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("MENOR QUE")
        elif quadList[i].operation == 9:
            
            if getValue(quadList[i].left_op) >= getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("MAYOR O IGUAL QUE")
        elif quadList[i].operation == 11:
            if getValue(quadList[i].left_op) <= getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("MENOR O IGUAL QUE")
        elif quadList[i].operation == 12:
            if getValue(quadList[i].left_op) == getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("IGUAL QUE")
        elif quadList[i].operation == 13:
            if getValue(quadList[i].left_op) != getValue(quadList[i].right_op):
                exeStack[-1].vars[quadList[i].tResult] = True
            else:
                exeStack[-1].vars[quadList[i].tResult] = False
            print("DIFERENTE QUE")
        elif quadList[i].operation == 15:
            print("WRITE: ", getValue(quadList[i].tResult))
        elif quadList[i].operation == 16:
            print("insert value: ")
            readValue(quadList[i].tResult)
            print("READ")
        elif quadList[i].operation == 17:
            i = quadList[i].tResult - 1
            print("GOTO")
        elif quadList[i].operation == 18:
            if getValue(quadList[i].left_op) == False:
                i = quadList[i].tResult - 1
            print("GOTOF")
        elif quadList[i].operation == 19:
            previousMemory = copy(exeStack[-1])
            paramExpression = True
            print("VENGAAAAA", previousMemory)
            exeStack.append(MemoryAllocator())
            print("ERA")
        elif quadList[i].operation == 20:
            assignParameter(quadList[i].left_op, quadList[i].tResult)
            print("PARAM")
        elif quadList[i].operation == 21:
            paramExpression = False
            exeGoSubStack.append(i) # we save where to jump back
            i = quadList[i].tResult - 1
            
            print("GOSUB")
        elif quadList[i].operation == 14:
            print("VERIFY")
        elif quadList[i].operation == 22:
            globalMemories[currentGlobalMemory].vars[quadList[i].left_op] =  getValue(quadList[i].tResult)
            
            print("RETURN")
        elif quadList[i].operation == 23:
            
            exeStack.pop()
            i = exeGoSubStack.pop()
    
            print("END FUNCTION")
        elif quadList[i].operation == 24:
            print("END PROGRAM")
        else:
            print("ERROR")

        i += 1


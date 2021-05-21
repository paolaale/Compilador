# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 21/05/2021

import semanticFunc as sF
from collections import deque
from MemoryAllocator import MemoryAllocator

exeStack = deque()
executionStack = dict()

currentGlobalMemory = "main";
currentLocalMemory = "";

globalMemories = dict()
globalMemories["main"] = MemoryAllocator()

initMemory = MemoryAllocator()
constDictionary = dict()

exeStack.append(initMemory)
exeGoSubStack = deque()
#print("CONST DICT: ", constDictionary)

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

    assignReadValue(container, newValue);

### Read and execute quadruples
def execute(quadList):
    global exeStack, globalMemories, exeGoSubStack
    dataInit()

    i = 0

    while quadList[i].operation != 24:

        if quadList[i].operation == 1:
            exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) + getValue(quadList[i].right_op)
            print("SUMA")
        elif quadList[i].operation == 2:
            exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) - getValue(quadList[i].right_op)
            print("RESTA")
        elif quadList[i].operation == 3:
            exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) * getValue(quadList[i].right_op)
            print("MULTIPLICACIÓN")
        elif quadList[i].operation == 4:
            exeStack[-1].vars[quadList[i].tResult] = getValue(quadList[i].left_op) / getValue(quadList[i].right_op)
            print("DIVISION")
        elif quadList[i].operation == 5:
            assignValue(quadList[i].left_op, quadList[i].tResult)
            print("ASSIGN")
        elif quadList[i].operation == 6:
            print("AND")
        elif quadList[i].operation == 7:
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
            readValue(quadList[i].tResult);
            print("READ")
        elif quadList[i].operation == 17:
            i = quadList[i].tResult - 1
            print("GOTO")
        elif quadList[i].operation == 18:
            if getValue(quadList[i].left_op) == False:
                i = quadList[i].tResult - 1
            print("GOTOF")
        elif quadList[i].operation == 19:
            exeStack.append(MemoryAllocator())
            print("ERA")
        elif quadList[i].operation == 20:
            print("PARAM")
        elif quadList[i].operation == 21:
            exeGoSubStack.append(i)
            exeGoSubStack.append(i) # we save where to jump back
            i = quadList[i].tResult - 1
            
           
            print("GOSUB")
        elif quadList[i].operation == 14:
            print("VERIFY")
        elif quadList[i].operation == 23:
            exeStack.pop()
            i = exeGoSubStack.pop()
            #print("quadToGoAfter: ", sF.direcClasses[currentGlobalMemory].c_funcs["getTotal"])
            print("END FUNCTION")
        elif quadList[i].operation == 24:
            print("END PROGRAM")
        else:
            print("ERROR")

        i += 1


class MemoryRange:
    def __init__(self, lowerLimit, upperLimit):

        self.currentVal = lowerLimit
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit

memoryDispatcher = {
    "global_int": MemoryRange(0, 3999),
    "global_t_int": MemoryRange(4000, 4999),
    "global_float": MemoryRange(5000, 8999),
    "global_t_float": MemoryRange(9000, 9999),
    "global_char": MemoryRange(10000, 12999),
    "global_bool": MemoryRange(13000, 15999),
    "global_t_bool": MemoryRange(16000, 16999),
    "local_int": MemoryRange(17000, 21999),
    "local_t_int": MemoryRange(22000, 22999),
    "local_float": MemoryRange(23000, 27999),
    "local_t_float": MemoryRange(28000, 28999),
    "local_char": MemoryRange(29000, 31999),
    "local_bool": MemoryRange(32000, 33999),
    "local_t_bool": MemoryRange(34000, 34999),
    "const_int": MemoryRange(35000, 35999),
    "const_float": MemoryRange(36000, 36999)

    # "objects_int: " MemoryRange(100000, 150000)

    # perro1 var a => 100001      100001
    # perro2 var a => 100002      100001
    # gato1 var a => 100003       100001


}

def get_space_avail(scope, varType, spaceNeed):
    global memoryDispatcher

    if scope == "temp":
        memoryRange = getMemoryTemp(varType)
    elif scope == "const":
        memoryRange = getMemoryConst(varType)
    else:
        memoryRange = getMemoryRangeOfDec(scope, varType)

    currentSpaceVal = memoryDispatcher[memoryRange].currentVal
    directToReturn = currentSpaceVal + spaceNeed - 1

    if directToReturn <= memoryDispatcher[memoryRange].upperLimit:
        memoryDispatcher[memoryRange].currentVal = currentSpaceVal + spaceNeed
        return directToReturn
    else:
        raise Exception("Too many variables")


# obtenemos el rango al que pertecene la memoria de variables en declaración
def getMemoryRangeOfDec(scope, varType):

    if scope == "vG":
        if varType == "int":
            return "global_int"
        elif varType == "float":
            return "global_float"
        else:
            return "global_char"
    else:
        if varType == "int":
            return "local_int"
        elif varType == "float":
            return "local_float"
        else:
            return "local_char"

def getMemoryTemp(varType):
    if varType == "int":
        return "local_t_int"
    elif varType == "float":
        return "local_t_float"
    else:
        return "local_t_bool"

def getMemoryConst(varType):
    if varType == "int":
        return "const_int"
    elif varType == "float":
        return  "const_float"

def reset_local_space():
    global memoryDispatcher

    memoryDispatcher["local_int"].currentVal = memoryDispatcher["local_int"].lowerLimit
    memoryDispatcher["local_t_int"].currentVal = memoryDispatcher["local_t_int"].lowerLimit
    memoryDispatcher["local_float"].currentVal = memoryDispatcher["local_float"].lowerLimit
    memoryDispatcher["local_t_float"].currentVal = memoryDispatcher["local_t_float"].lowerLimit
    memoryDispatcher["local_char"].currentVal = memoryDispatcher["local_char"].lowerLimit
    memoryDispatcher["local_bool"].currentVal = memoryDispatcher["local_bool"].lowerLimit
    memoryDispatcher["local_t_bool"].currentVal = memoryDispatcher["local_t_bool"].lowerLimit

def reset_global_space():
    global memoryDispatcher
    
    memoryDispatcher["global_int"].currentVal = memoryDispatcher["global_int"].lowerLimit
    memoryDispatcher["global_t_int"].currentVal = memoryDispatcher["global_t_int"].lowerLimit
    memoryDispatcher["global_float"].currentVal = memoryDispatcher["global_float"].lowerLimit
    memoryDispatcher["global_t_float"].currentVal = memoryDispatcher["global_t_float"].lowerLimit
    memoryDispatcher["global_char"].currentVal = memoryDispatcher["global_char"].lowerLimit
    memoryDispatcher["global_bool"].currentVal = memoryDispatcher["global_bool"].lowerLimit
    memoryDispatcher["global_t_bool"].currentVal = memoryDispatcher["global_t_bool"].lowerLimit
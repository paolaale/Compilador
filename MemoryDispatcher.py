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
}

def get_space_avail(scope, varType, spaceNeed):

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

    if scope == "global":
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

def update_space_avail(varType):
    memoryDispatcher[varType].currentVal = memoryDispatcher[varType].lowerLimit

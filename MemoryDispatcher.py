# Class Memory range that contains the lower, upper and current value of a Range of memory addresses
class MemoryRange:
    def __init__(self, lowerLimit, upperLimit):

        self.currentVal = lowerLimit
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit


# dictionary of Memory Ranges, that helps to differiante all the scopes and vars types
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
    "const_float": MemoryRange(36000, 36999),
    "const_char": MemoryRange(37000, 37999),
    "const_string": MemoryRange(38000, 38999)
}

# Counter of classes instances
countOfInstances = 0

# function to assign the corresponding memory reference to a variable, receiving the scope varType
# and the space needed for that variable that could be a matrix or array
def get_space_avail(scope, varType, spaceNeed):
    global memoryDispatcher, countOfInstances

    # First we get the memory range according to the scope
    if scope == "temp":
        memoryRange = getMemoryTemp(varType)
    elif scope == "const":
        memoryRange = getMemoryConst(varType)
    else:
        memoryRange = getMemoryInDeclaration(scope, varType)

    # if the variable is an object, we specify directly its memory reference
    if memoryRange == "obj_instance":
        countOfInstances += 1
        return countOfInstances

    # if not an object, the memory reference for the variable is returned and the counter of
    # variables in the corresponding range (currentSpaceVal) is returned
    else: 
        currentSpaceVal = memoryDispatcher[memoryRange].currentVal
        directToReturn = currentSpaceVal + spaceNeed - 1

        if directToReturn <= memoryDispatcher[memoryRange].upperLimit:
            memoryDispatcher[memoryRange].currentVal = currentSpaceVal + spaceNeed
            return directToReturn
        else:
            raise Exception("Too many variables")


# We obtain the memory range that belongs to the corresponding declared variable
def getMemoryInDeclaration(scope, varType):

    if scope == "vG":
        if varType == "int":
            return "global_int"
        elif varType == "float":
            return "global_float"
        elif varType == "char":
            return "global_char"
        else:
            return "obj_instance"
    else:
        if varType == "int":
            return "local_int"
        elif varType == "float":
            return "local_float"
        elif varType == "char":
            return "local_char"
        else:
            return "obj_instance"

# We obtain the memory range that belongs to the corresponding temporal variable
def getMemoryTemp(varType):
    if varType == "int":
        return "local_t_int"
    elif varType == "float":
        return "local_t_float"
    else:
        return "local_t_bool"

# We obtain the memory range that belongs to the corresponding constant variable
def getMemoryConst(varType):
    if varType == "int":
        return "const_int"
    elif varType == "float":
        return  "const_float"
    elif varType == "char":
        return "const_char"
    else:
        return "const_string"

# Function to reset all the local memory ranges to their initial currentVal
def reset_local_space():
    global memoryDispatcher

    memoryDispatcher["local_int"].currentVal = memoryDispatcher["local_int"].lowerLimit
    memoryDispatcher["local_t_int"].currentVal = memoryDispatcher["local_t_int"].lowerLimit
    memoryDispatcher["local_float"].currentVal = memoryDispatcher["local_float"].lowerLimit
    memoryDispatcher["local_t_float"].currentVal = memoryDispatcher["local_t_float"].lowerLimit
    memoryDispatcher["local_char"].currentVal = memoryDispatcher["local_char"].lowerLimit
    memoryDispatcher["local_bool"].currentVal = memoryDispatcher["local_bool"].lowerLimit
    memoryDispatcher["local_t_bool"].currentVal = memoryDispatcher["local_t_bool"].lowerLimit

# Function to reset all the global memory ranges to their initial currentVal
def reset_global_space():
    global memoryDispatcher
    
    memoryDispatcher["global_int"].currentVal = memoryDispatcher["global_int"].lowerLimit
    memoryDispatcher["global_t_int"].currentVal = memoryDispatcher["global_t_int"].lowerLimit
    memoryDispatcher["global_float"].currentVal = memoryDispatcher["global_float"].lowerLimit
    memoryDispatcher["global_t_float"].currentVal = memoryDispatcher["global_t_float"].lowerLimit
    memoryDispatcher["global_char"].currentVal = memoryDispatcher["global_char"].lowerLimit
    memoryDispatcher["global_bool"].currentVal = memoryDispatcher["global_bool"].lowerLimit
    memoryDispatcher["global_t_bool"].currentVal = memoryDispatcher["global_t_bool"].lowerLimit
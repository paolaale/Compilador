import semanticFunc as sF

### Memory added to variable tables test ###
def printMemoryInDeclaration():
    print("insert num of vals to test memory: ");
    numOfVars = int(input())
    i = 0

    while (i < numOfVars):
        print("insert name of class, function and var: ");
        className = input()
        functName = input()
        varName = input()
        print("memRef of Var ", sF.direcClasses.get(className).c_funcs.get(functName).f_vars[varName].memRef);
        i = i + 1;
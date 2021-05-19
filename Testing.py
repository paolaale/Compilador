import semanticFunc as sF

### Memory added to variable tables test ###
def printMemoryInDeclaration():
    print("insert num of vals to test memory: ");
    numOfVars = int(input())
    i = 0

    while (i < numOfVars):
        print("insert name of class: ");
        className = input()
        print("insert name of function: ");
        functName = input()
        print("insert name of var: ");
        varName = input()
        print("memRef of Var ", sF.direcClasses.get(className).c_funcs.get(functName).f_vars[varName].memRef);
        i = i + 1;

def printFunctsTable():
    print("insert num of funcs tables to check: ");
    numOfVars = int(input())
    i = 0

    while (i < numOfVars):
        print("insert name of class, function and var: ");
        print("insert name of class: ");
        className = input()
        
        print("Funciontts of class: ", sF.direcClasses.get(className).c_funcs);
        i = i + 1;

def printVarsTable():
    print("insert num of vars tables to check: ");
    numOfVars = int(input())
    i = 0

    while (i < numOfVars):
        print("insert name of class, function and var: ");
        print("insert name of class: ");
        className = input()
        print("insert name of function: ");
        functName = input()
        print("VarsTable of function: ", sF.direcClasses.get(className).c_funcs.get(functName).f_vars);
        i = i + 1;
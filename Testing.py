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
    
    # print("var globales de main: ", sF.direcClasses.get("main").c_funcs.get("vG").f_vars);
    # print("var global p: ", sF.direcClasses.get("main").c_funcs.get("vG").f_vars["p"].memRef);
    # print("var global k: ", sF.direcClasses.get("main").c_funcs.get("vG").f_vars["k"].memRef);

    # print("var local rubs: ", sF.direcClasses.get("main").c_funcs.get("getTotal").f_vars["rubs"].memRef);
    # print("var local paola: ", sF.direcClasses.get("main").c_funcs.get("getTotal").f_vars["paola"].memRef);
    # print("var local omar: ", sF.direcClasses.get("main").c_funcs.get("getTotal").f_vars["omar"].memRef);
    # print("var local joe: ", sF.direcClasses.get("main").c_funcs.get("getTotal").f_vars["joe"].memRef);
    # print("variables local init main: ",  sF.direcClasses.get("main").c_funcs.get("init").f_vars);
    # print("variables local init main var p: ",  sF.direcClasses.get("main").c_funcs.get("init").f_vars["p"].memRef);
    # print("variables local init main var g: ",  sF.direcClasses.get("main").c_funcs.get("init").f_vars["g"].memRef);
    # print("variables local init main var harry: ",  sF.direcClasses.get("main").c_funcs.get("init").f_vars["harry"].memRef);
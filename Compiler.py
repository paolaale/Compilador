import parser as parserOfCompiler
import semanticFunc as sF
import VirtualMachine as vM

if __name__ == '__main__':
    
    # Read file
    doc = input()
    fileData = open(doc,'r')

    text = ""
    
    # Read every line of the file
    for line in fileData:
        try:
            text = text + line.strip() # Delete all white spaces
        except EOFError:
            break

    # Text that has all the code        
    if text:
        
        result = parserOfCompiler.parser.parse(text) # Compile the code
        
        #sF.printQuadruples()
        #print("------------------------------------")
        #sF.printMemoryQuadruples()
        #print("------------------------------------")
        vM.execute(sF.quadMEM)
        
        if result != None:
            print("Program accepted") # If execution went well
        else:
            print("Program failed")
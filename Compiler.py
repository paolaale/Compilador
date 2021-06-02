import parser as parserOfCompiler
import semanticFunc as sF
import VirtualMachine as vM

if __name__ == '__main__':
    
    # Read file
    doc = input()
    fileData = open(doc,'r')

    text = ""

    for line in fileData:
        try:
            text = text + line.strip()
        except EOFError:
            break
            
    if text:
        result = parserOfCompiler.parser.parse(text)
        
        #sF.printQuadruples()
        #print("------------------------------------")
        #sF.printMemoryQuadruples()
        #print("------------------------------------")
        vM.execute(sF.quadMEM)
        
        if result != None:
            print("Program accepted")
        else:
            print("Program failed")
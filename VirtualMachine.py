# Proyecto compiladores, Grupo 02
# Equipo 23, orientado a objetos
# Paola Villarreal - A00821971
# Alan Zavala - A01338448
# Fecha: 21/05/2021

def execute(quadList):
    
    i = 0

    for quad in quadList:

        if quad.operation == '+':
            quad.tResult = int(quad.left_op) + int(quad.right_op)
        elif quad.operation == '-':
            quad.tResult = int(quad.left_op) - int(quad.right_op)
        elif quad.operation == '*':
            quad.tResult = int(quad.left_op) * int(quad.right_op)
        elif quad.operation == '/':
            quad.tResult = int(quad.left_op) / int(quad.right_op)
        elif quad.operation == '=':
            quad.tResult = int(quad.left_op)
        elif quad.operation == 'and':
            print("AND")
        elif quad.operation == 'or':
            print("OR")
        elif quad.operation == '>':
            print("MAYOR QUE")
        elif quad.operation == '<':
            print("MENOR QUE")
        elif quad.operation == '>=':
            print("MAYOR O IGUAL QUE")
        elif quad.operation == '<=':
            print("MENOR O IGUAL QUE")
        elif quad.operation == '==':
            print("IGUAL QUE")
        elif quad.operation == '!=':
            print("DIFERENTE QUE")
        elif quad.operation == 'WRITE':
            print("WRITE")
        elif quad.operation == 'READ':
            print("READ")
        elif quad.operation == 'GOTO':
            print("GOTO")
        elif quad.operation == 'GOTOF':
            print("GOTOF")
        elif quad.operation == 'GOTOV':
            print("GOTOV")
        elif quad.operation == 'ERA':
            print("ERA")
        elif quad.operation == 'PARAM':
            print("PARAM")
        elif quad.operation == 'GOSUB':
            print("GOSUB")
        elif quad.operation == 'VERIFY':
            print("GOSUB")
        elif quad.operation == 'END FUNCTION':
            print("END FUNCTION")
        elif quad.operation == 'END PROGRAM':
            print("END PROGRAM")
        else:
            print("ERROR")

        i += 1
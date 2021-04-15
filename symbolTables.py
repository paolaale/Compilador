class Functions: #key = name of the var, value = instance of Vars class
    
    def __init__(self, f_type):
        self.f_type = f_type
        self.f_vars = {}
    
class Vars:
    v_type = ""
    value = ""
    rows = 0
    cols = 0

    def __init__(self, v_type, rows, cols):
        self.v_type = v_type
        self.rows = rows
        self.cols = cols
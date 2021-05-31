class Vars:  #key = name of the var, value = type of the var, size if is array or matrix 

    v_type = ""
    memRef = ""
    rows = 0
    cols = 0

    def __init__(self, v_type, rows, cols, memRef):
        self.v_type = v_type
        self.rows = rows
        self.cols = cols
        self.memRef = memRef
        self.lowerMemRef = memRef - abs(int(rows) * int(cols)) + 1


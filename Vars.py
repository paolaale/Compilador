class Vars:
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
"""     
    def __init__(self, v_type, rows, cols, lowerMemRef, upperMemRef):
        self.v_type = v_type
        self.rows = rows
        self.cols = cols
        self.lowerMemRef = lowerMemRef     
        self.upperMemRef = upperMemRef """ 

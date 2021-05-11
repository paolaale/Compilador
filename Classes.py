from Functions import Functions

class Classes: #key = name of the class, value = parent and instance of Function class
    
    def __init__(self, c_inherits, c_parent):
        self.c_inherits = c_inherits
        self.c_parent = c_parent
        self.c_funcs = {"vG": Functions("global", 0, None)}
    
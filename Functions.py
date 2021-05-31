#key = name of the function, 
# value = type of function, numer of parameters and instance of Vars class
class Functions:
    
    def __init__(self, f_type, f_params_type, f_number_params, f_start_quadruple):
        self.f_type = f_type
        self.f_params_type = f_params_type
        self.f_number_params = f_number_params
        self.f_start_quadruple = f_start_quadruple
        self.f_vars = {}
        self.f_params_memRefs = []
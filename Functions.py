class Functions: #key = name of the var, value = instance of Vars class
    
    def __init__(self, f_type, f_params_type, f_number_params, f_start_quadruple):
        self.f_type = f_type
        self.f_params_type = f_params_type
        self.f_number_params = f_number_params
        self.f_start_quadruple = f_start_quadruple
        self.f_vars = {}
        self.f_params_memRefs = []
        #!!!! probablemente agregar aquí la memoria que esta clase necesitará cada funcióon, incluyendo
        #!!!! la memoria necesaria para las variables globales.
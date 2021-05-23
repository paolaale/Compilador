class MemoryAllocator:

    def __init__(self, lowerLimit, upperLimit):
        self.ints = dict()
        self.floats = dict()
        self.chars = dict()
        self.bools = dict()

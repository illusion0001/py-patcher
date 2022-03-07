from src.archtype.types.types import types

class Cell:

    def __init__(self):
        self.baseAddr = 0x10000
        self.endian = 'big'

    def convertData(self, var_type, offset, value):
        return {
            'offset': offset - self.baseAddr,
            'value': types(self.endian).convert(value, var_type)
        }

class Generic:

    def __init__(self):
        self.endian = 'little'

    def convertData(self, var_type, offset, value):
        return {
            'offset': offset,  # - self.baseAddr
            'value': types(self.endian).convert(value, var_type)  # self.types[var_type]().convert(value)
        }

class Orbis:

    def __init__(self):
        self.baseAddr = 0x3FC000
        self.endian = 'little'

    def convertData(self, var_type, offset, value):
        return {
            'offset': offset - self.baseAddr,
            'value': types(self.endian).convert(value, var_type)
        }

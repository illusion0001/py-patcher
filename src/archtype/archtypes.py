from src.archtype.shared.shared_datatypes import shared_utf8, shared_byte_array, shared_byte
from src.archtype.be.be_datatypes import be_float32, be_float64, be_bytes16, be_bytes32, be_bytes64
from src.archtype.le.le_datatypes import le_float32, le_float64, le_bytes16, le_bytes32, le_bytes64

class Cell():

    def __init__(self):
        self.baseAddr = 0x10000
        self.types = {
            "bytes" : shared_byte_array,
            "byte" : shared_byte,
            "be16" : be_bytes16,
            "be32" : be_bytes32,
            "be64" : be_bytes64,
            "bef32" : be_float32,
            "bef64" : be_float64,
            "utf8" : shared_utf8
        }

    def convertData(self, var_type, offset, value):
        return {
            'offset': offset - self.baseAddr,
            'value': self.types[var_type]().convert(value)
        }

class Generic():

    def __init__(self):
        #self.baseAddr = 0x0
        self.types = {
            "bytes" : shared_byte_array,
            "byte" : shared_byte,
            "le16" : le_bytes16,
            "le32" : le_bytes32,
            "le64" : le_bytes64,
            "lef32" : le_float32,
            "lef64" : le_float64,
            "utf8" : shared_utf8
        }

    def convertData(self, var_type, offset, value):
        return {
            'offset': offset, # - self.baseAddr
            'value': self.types[var_type]().convert(value)
        }

class Orbis():

    def __init__(self):
        self.baseAddr = 0x3FC000
        self.types = {
            "bytes" : shared_byte_array,
            "byte" : shared_byte,
            "le16" : le_bytes16,
            "le32" : le_bytes32,
            "le64" : le_bytes64,
            "lef32" : le_float32,
            "lef64" : le_float64,
            "utf8" : shared_utf8
        }

    def convertData(self, var_type, offset, value):
        return {
            'offset': offset - self.baseAddr,
            'value': self.types[var_type]().convert(value)
        }

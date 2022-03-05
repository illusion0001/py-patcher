import struct

class le_bytes16:
    def convert(self,value):
          return value.to_bytes(2, 'little')

class le_bytes32:
    def convert(self,value):
          return value.to_bytes(4, 'little')

class le_bytes64:
    def convert(self,value):
          return value.to_bytes(8, 'little') 

class le_float32: # https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex
    def convert(self,value):
        float = float_to_hex(value)
        return float.to_bytes(4, 'little')

def float_to_hex(f):
    return (struct.unpack('<I', struct.pack('<f', f))[0])

class le_float64:
    def convert(self,value):
        double = double_to_hex(value)
        return double.to_bytes(8, 'little')

def double_to_hex(f):
    return (struct.unpack('<Q', struct.pack('<d', f))[0])

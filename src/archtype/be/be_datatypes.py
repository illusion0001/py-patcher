import struct

class be_bytes16:
    def convert(self,value):
          return value.to_bytes(2, 'big')

class be_bytes32:
    def convert(self,value):
          return value.to_bytes(4, 'big')

class be_bytes64:
    def convert(self,value):
          return value.to_bytes(8, 'big')

class be_float32:
    def convert(self,value):
        float = float_to_hex(value)
        return float.to_bytes(4, 'big')

def float_to_hex(f): # https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex
    return (struct.unpack('<I', struct.pack('<f', f))[0])

class be_float64:
    def convert(self,value):
        double = double_to_hex(value)
        return double.to_bytes(8, 'big')

def double_to_hex(f):
    return (struct.unpack('<Q', struct.pack('<d', f))[0])

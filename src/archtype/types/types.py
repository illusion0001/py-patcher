import struct

class types:

    def __init__(self, endian):
        self.endian = endian
        self.typeDic = {
            'byte': self.byte,
            'bytes': self.byte_array,
            'bytes16': self.bytes16,
            'bytes32': self.bytes32,
            'bytes64': self.bytes64,
            'float32': self.float32,
            'float64': self.float64,
            'utf8': self.utf8,
            'utf16': self.utf16
        }

    def convert(self, value, type):
        return self.typeDic[type](value)

    def byte_array(self, value):
        return bytearray.fromhex(value)

    def byte(self, value):
        return value.to_bytes(1, 'little')

    def bytes16(self, value):
        return value.to_bytes(2, self.endian)

    def bytes32(self, value):
        return value.to_bytes(4, self.endian)

    def bytes64(self, value):
        return value.to_bytes(8, self.endian)

    def float32(self, value):
        float = self.__float_to_hex(value)
        return float.to_bytes(4, self.endian)

    def float64(self, value):
        double = self.__double_to_hex(value)
        return double.to_bytes(8, self.endian)

    def utf8(self, value):
        return value.encode('utf-8')

    def utf16(self, value):
        return value.encode('utf-16le')

    # https://stackoverflow.com/questions/23624212/how-to-convert-a-float-into-hex
    def __float_to_hex(self, f):
        return (struct.unpack('<I', struct.pack('<f', f))[0])

    def __double_to_hex(self, f):
        return (struct.unpack('<Q', struct.pack('<d', f))[0])

class shared_byte:
    def convert(self,value):
          return value.to_bytes(1, 'little')

class shared_byte_array:
    def convert(self,value):
          return bytearray.fromhex(value)

class shared_utf8:
    def convert(self,value):
          return value.encode('utf-8')


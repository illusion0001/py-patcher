import sys

offset_hex = sys.argv[2]
hexadecimal_string = sys.argv[3]
byte_array = bytearray.fromhex(hexadecimal_string)
print("Input file:  ", sys.argv[1])
print("Input array: ", hexadecimal_string)
print(byte_array)

path = sys.argv[1]
offset = (int(offset_hex, 0))

# todo make this as argument
ElfAddrCell = False

with open(path, 'r+b') as f:
    # normal path
    f.seek(offset, 0)
    # cell path
    if ElfAddrCell == True:
        f.seek(offset-65536, 0)
    f.write(byte_array)

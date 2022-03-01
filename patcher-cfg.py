import configparser
import sys

# usage: inputfile.elf input.cfg

Config = configparser.ConfigParser(strict=False)
config = configparser.ConfigParser()
config.read(sys.argv[2])

def patchfile():
    hexadecimal_string = str(patch)
    offset_hex = str(addr)
    byte_array = bytearray.fromhex(hexadecimal_string)
    #print("Input array: ", hexadecimal_string)
    path = sys.argv[1]
    offset = (int(offset_hex, 0))
    # todo pass this from cfg
    config.getboolean("patch", "ElfAddrCell")
    with open(path, 'r+b') as f:
        # normal path
        f.seek(offset, 0)
        # cell path
        if elfaddr == True:
            f.seek(offset-65536, 0)
        f.write(byte_array)

# cursed, todo make this iterate
title = config['patch']['name']
addr = config['patch']['addrr']
patch = config['patch']['value']
elfaddr = config.getboolean("patch", "ElfAddrCell")
print(f'PatchTitle: {title}')
print(f'Address:    {addr}')
print(f'Patch:      {patch}')
print(f'UsePS3Addr: {elfaddr}')
patchfile()
# title = config['patch1']['name']
# addr = config['patch1']['addrr']
# patch = config['patch1']['value']
# elfaddr = config.getboolean("patch1", "ElfAddrCell")
# print(f'PatchTitle: {title}')
# print(f'Address:    {addr}')
# print(f'Patch:      {patch}')
# print(f'UsePS3Addr: {elfaddr}')
# patchfile()

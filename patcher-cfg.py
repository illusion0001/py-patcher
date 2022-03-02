import configparser
import sys

# usage: inputfile.elf input.cfg

config = configparser.ConfigParser()
config.read(sys.argv[2])

def patchfile():
    hexadecimal_string = str(patch)
    offset_hex = str(addr)
    byte_array = bytearray.fromhex(hexadecimal_string)
    path = sys.argv[1] # input
    offset = (int(offset_hex, 0))
    section.getboolean('ElfAddrCell')
    with open(path, 'r+b') as f:
        # normal path
        f.seek(offset, 0)
        # cell elf path
        if elfaddr == True:
            f.seek(offset-65536, 0)
        f.write(byte_array)

for section in config.sections():
    section    = config[section]
    title      = section.get('name')
    addr       = section.get('addrr')
    patch      = section.get('value')
    elfaddr    = section.getboolean('ElfAddrCell')
    patch_this = section.getboolean('PatchEnabled')
    print(f'PatchTitle: {title}')
    print(f'Address:    {addr}')
    print(f'Patch:      {patch}')
    print(f'UsePS3Addr: {elfaddr}')
    print(f'Enabled:    {patch_this}')
    if elfaddr == True:
        print(f'Patch: "{title}" using CELL ELF address base.')
    if patch_this == True:
        patchfile()
        print(f'Patch: "{title}" Patched.')
    else:
        print(f'Patch: "{title}" skipped.')

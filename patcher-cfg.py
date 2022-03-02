import configparser
import sys

# usage: inputfile.elf input.cfg

# https://stackoverflow.com/questions/9876059/parsing-configure-file-with-same-section-name-in-python
from collections import OrderedDict

class multidict(OrderedDict):
    _unique = 0   # class variable

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += str(self._unique)
        OrderedDict.__setitem__(self, key, val)

config = configparser.ConfigParser(defaults=None, dict_type=multidict, strict=False)
config = configparser.ConfigParser()
config.read(sys.argv[2])

def patchfile():
    hexadecimal_string = str(patch)
    offset_hex = str(addr)
    byte_array = bytearray.fromhex(hexadecimal_string)
    path = sys.argv[1]
    offset = (int(offset_hex, 0))
    section.getboolean('ElfAddrCell')
    with open(path, 'r+b') as f:
        # normal path
        f.seek(offset, 0)
        # cell path
        if elfaddr == True:
            f.seek(offset-65536, 0)
        f.write(byte_array)

for section in config.sections():
    section = config[section]
    title = section.get('name')
    addr = section.get('addrr')
    patch = section.get('value')
    elfaddr = section.getboolean('ElfAddrCell')
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

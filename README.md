# py-patcher

Simple Binary Patching in Python3

## Usage

CLI:

```bash
patcher.py [filepath] [offset] [byte_array] # i.e ca1f00d or "ca 1f 00 0d"
# patcher.py 1.elf 0xCD40 "60000000"
# patcher.py 1.elf 0xCD44 "60 00 00 00"
```

CFG:

```bash
patcher.py [filepath] [cfgpath]
# patcher.py 1.elf input.cfg
# content of .cfg file

# [patch]
# ElfAddrCell=False
# name = Dummy Patch Name
# addrr = 0xCA7F00D
# value = CA7F00D
```

# Credits

[aerosoul94](https://github.com/aerosoul94)

Shadow

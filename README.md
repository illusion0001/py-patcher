# py-patcher

Simple Binary Patching in Python3

# Features

Unlimited byte array (CLI and yml)

Config like parsing support (yml only)

## Usage

CLI:

```
patcher.py [filepath] [offset] [byte_array] # i.e ca1f00d or "ca 1f 00 0d"
# patcher.py 1.elf 0xCD40 "60000000"
# patcher.py 1.elf 0xCD44 "60 00 00 00"
```

yml: see syntax in [example.yml](example.yml)

```
patcher-yml -h
usage: patcher-yml.py [-h] -f FILE -c CONFIG
example: patcher-yml.py -f example.elf -c example.yml

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  The ELF file we need to patch.
  -c CONFIG, --config CONFIG
                        The configuration file.
```

# Credits

ShadowDog

[aerosoul94](https://github.com/aerosoul94)

## Todo-list

Add valid executable checks

Support big endian float

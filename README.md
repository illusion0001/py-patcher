# py-patcher

Simple Binary Patching in Python3

# Features

Unlimited byte array (CLI and yml)

Config like parsing support (yml only)

## Usage

CLI:

```bash
patcher.py [filepath] [offset] [byte_array] # i.e ca1f00d or "ca 1f 00 0d"
# patcher.py 1.elf 0xCD40 "60000000"
# patcher.py 1.elf 0xCD44 "60 00 00 00"
```

yml: see syntax in [example.yml](example.yml)

```bash
patcher-yml.py [filepath] [ymlpath]
```

# Credits

ShadowDog

[aerosoul94](https://github.com/aerosoul94)

## Todo-list

Support big endian float

Help message when no arguments are provided

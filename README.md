# py-patcher

Simple Binary Patching in Python3

## Usage

```bash
patcher.py [filepath] [offset] [byte_array] # i.e ca1f00d or "ca 1f 00 0d"
# patcher.py 1.elf 0xCD40 "60000000"
# patcher.py 1.elf 0xCD44 "60 00 00 00"
```

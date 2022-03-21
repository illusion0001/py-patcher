# py-patcher

Simple Binary Patching for console games in Python.

Latest binaries: https://github.com/illusion0001/py-patcher/releases/latest

[![Build and test PyPatcher](https://github.com/illusion0001/py-patcher/actions/workflows/build_and_test.yml/badge.svg)](https://github.com/illusion0001/py-patcher/actions/workflows/build_and_test.yml)

# Features

- Config like parsing support.
- Supports big and little endian architecture. (PS3 and PS4)
- Easy to read syntaxes.

### Architectures

- Generic - for legacy direct file address patches
- Cell - for transferring RPCS3 patches to real console
- Orbis - for transferring new PS4 patches to real console

### Types

- utf8 - text string (must be enclosed with quotation marks. i.e ( `"hello world!"` )
- bytes - byte array (i.e `90 90 90 90` or `90909090` )
- byte - 1 byte
- bytes16 - 2 bytes
- bytes32 - 4 bytes
- bytes64 - 8 bytes
- float32 - single 32 bit float
- float64 - double 64 bit float

See syntax in [example.yml](data/example.yml)

### Program usage

```
launcher.py -h

Usage: launcher.py [-h] -f FILE -c CONFIG [-v] [-od] [-o OUTPUTPATH] [-ci]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify file to be patched.
  -c CONFIG, --config CONFIG
                        Specify patch file.
  -v, --verbose         Enable Verbose Mode.
  -od, --outputdate     Append date and time to output directory.
  -o OUTPUTPATH, --outputpath OUTPUTPATH
                        Specify output file path.
  -ci, --cibuild        For running tests on buildbot.
```

# Credits
- ShadowDog
- [aerosoul94](https://github.com/aerosoul94)

# Todo-list

- [ ] Move Patch Enabled field to auto generated file

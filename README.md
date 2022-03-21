# py-patcher

Simple Binary Patching for console games in Python.

[![Build and test PyPatcher](https://github.com/illusion0001/py-patcher/actions/workflows/build_and_test.yml/badge.svg)](https://github.com/illusion0001/py-patcher/actions/workflows/build_and_test.yml)

# Features

- Config like parsing support.
- Supports big and little endian architecture. (PS3 and PS4)
- Easy to read syntaxes.

## Usage

See syntax in [example.yml](data/example.yml)

```
launcher.py -husage: launcher.py [-h] -f FILE -c CONFIG [-v] [-od] [-o OUTPUTPATH] [-ci]

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

## Todo-list

- [ ] Move Patch Enabled field to auto generated file

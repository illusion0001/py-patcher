# [py-patcher](../../../../illusion0001/py-patcher)

Simple Binary Patching for console games in Python.

Latest binaries: https://github.com/illusion0001/py-patcher-bin/releases/latest

[![Build and test PyPatcher](https://github.com/illusion0001/py-patcher/actions/workflows/build_and_test.yml/badge.svg)](https://github.com/illusion0001/py-patcher/actions/workflows/build_and_test.yml)

# Features

- Download/Update [patch](https://github.com/illusion0001/illusion0001.github.io/tree/main/_patch0) files with `-dl` flag.
- Config like parsing support.
- Supports big and little endian architecture. (PS3 and PS4)
- Easy to read syntaxes.

### Architectures

- Generic - for legacy direct file address patches
- Cell - for transferring RPCS3 patches to real console
- Orbis - for transferring new PS4 patches to real console

### Types

- utf8 - text string (must be enclosed with quotation marks. i.e  `"hello world!"` )
- utf16 - text string (must be enclosed with quotation marks. i.e `"hello world!"` )
- bytes - byte array (must be enclosed with quotation marks. i.e `"90 90 90 90"` or `"90909090"` )
- byte - 1 byte <!-- (`0x12`/`18`) -->
- bytes16 - 2 bytes <!-- (`0x1234`/`4660`) -->
- bytes32 - 4 bytes <!-- (`0x12345678`/`305419896`) -->
- bytes64 - 8 bytes <!-- (`0x1234567890abcdef`/`1311768467294899695`) -->
- float32 - single 32 bit float <!-- (`1.0`) -->
- float64 - double 64 bit float <!-- (`1.0000`) -->

Example (scroll down for more info): https://github.com/illusion0001/py-patcher/blob/7166320afeffe8fadd9715579b5fcf909ce4fb86/data/example.yml#L26-L54

### Program usage

```
launcher.py -h
usage: launcher.py [-h] -f FILE -p PATCH [-v] [-od] [-o OUTPUT_PATH] [-ci] [-y]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Specify file to be patched.
  -p PATCH, --patch PATCH
                        Specify patch file.
  -v, --verbose         Enable Verbose Mode.
  -od, --output_date    Append date and time to output directory.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Specify output file path.
  -ci, --ci_build       For running tests on buildbot.
  -y, --always_yes      Always skip confirmation prompts.
  -dl, --download_patch
                        Download/Update patch files.
```

# Credits
- ShadowDog
- [aerosoul94](https://github.com/aerosoul94)

# Todo-list

- [ ] Move Patch Enabled field to auto generated file

import sys
import os
import coloredlogs
import shutil
import logging
import yaml
from datetime import datetime

# usage: input.elf input.yml
# todo:  help message

logging.basicConfig()
logs = logging.getLogger(__name__)
coloredlogs.install(level=logging.INFO, logger=logs)

def patchfile(type, offset_pre, hexadecimal_string, iscell, isorbis, out, count):
    byte_array = bytearray.fromhex(hexadecimal_string)
    path = out
    offset_post = offset_pre  # need to be declared before use
    logs.debug('\nPatch type: {}'.format(type))
    with open(path, 'r+b') as f:
        # normal path
        f.seek(offset_post, 0)
        if iscell == True and isorbis == True:
            logs.error("\n"
                       "==============================================================\n"
                       "ERROR: Cannot use two architecture at the same time, aborting!\n"
                       "==============================================================\n")
            os.abort()
        # cell path
        if iscell == True:
            offset_post = offset_pre - 0x10000
            f.seek(offset_post, 0)
        # orbis path
        elif isorbis == True:
            offset_post = offset_pre - 0x3FC000 # disabled aslr addr - file addr
            f.seek(offset_post, 0)
        f.write(byte_array)
        logs.info(
            "\nApplied Patch Line {} in file: {}".format(count, out))

with open(sys.argv[2]) as fh:
    read_data = yaml.safe_load(fh)
    input = sys.argv[1]
    out = os.path.join(os.getcwd(), datetime.now().strftime(
        '{}-%Y-%m-%d-%H-%M-%S/{}'.format(os.path.basename(input),os.path.basename(input))))
    logs.info('\nInput file: {}'.format(out))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(input, out)
    for i in range(0, len(read_data)):
        # Checking desired verbosity level
        if read_data[i]['verbose']:
            coloredlogs.set_level(logging.DEBUG)
        # Print Author, Description ...
        logs.info("\n"
                  "=====================\n"
                  "= Game Title    : {}\n"
                  "= Patch Name    : {}\n"
                  "= Patch Author  : {}\n"
                  "= Patch Note    : {}\n"
                  "= Patch Enabled : {}\n"
                  "====================="
            .format(
            read_data[i]['game'],
            read_data[i]['name'],
            read_data[i]['author'],
            read_data[i]['note'],
            read_data[i]['enabled']))
        count = 1
        if read_data[i]['enabled'] == False:
            logs.warning('\nPatch: "{}" for "{}" is disabled and will be skipped.'
                .format(
                read_data[i]['name'],
                read_data[i]['game'], ))
        else:
            for patch_data in read_data[i]['patch_list']:
                count += 1
                logs.info("\nApplying patch: {}".format(count))
                logs.debug("\n"
                           "====================\n"
                           "= Patch Type    : {}\n"
                           "= Offset (Real) : {}\n"
                           "= Value         : {}\n"
                           "= UseElfAddr    : {}\n"
                           "= IsOrbis       : {}\n"
                           "= OutFile       : {}\n"
                           "= Line          : {}\n"
                           "====================".format(patch_data[0], hex(patch_data[1]), patch_data[2],
                                                           patch_data[3], patch_data[4], out, count))
                patchfile(patch_data[0], patch_data[1], patch_data[2], patch_data[3], patch_data[4], out, count)

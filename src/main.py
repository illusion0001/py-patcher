import os
import coloredlogs
import shutil
import logging as logs
import yaml
from datetime import datetime

from src.archtype.archtypes import Cell, Generic, GenericOrbis, Orbis

# Easily load different architectures
arch_dic = {
    "CELL": Cell,
    "GENERIC": Generic,  # for direct and array of bytes
    # (AOB pattern find and replace)
    "ORBIS": Orbis,
    "GENERIC_ORBIS": GenericOrbis
}

def patchfile(offset, value, out, count):
    # Open and patch the output file
    with open(out, 'r+b') as f:
        logs.debug('\nfile offset: {}'
                   '\ninput: {}'.format(hex(offset), value))
        f.seek(offset, 0)
        f.write(value)
        logs.info(
            "\nApplied Patch Line {} in file: {}".format(count, out))

def headercheck(archs, elf):
    header = open(elf, "rb")
    cell_valid_header = b'\x7F\x45\x4C\x46\x02\x02\x01\x66'
    orbis_valid_header1 = b'\x7F\x45\x4C\x46\x02\x01\x01\x09'
    orbis_valid_header2 = b'\x2F\x6C\x69\x62\x65\x78\x65\x63\x2F\x6C\x64\x2D\x65\x6C\x66\x2E\x73\x6F\x2E\x31'
    if archs == 'cell':
        elf_header = header.read(8)
        if elf_header == cell_valid_header:
            logs.debug("\n"
                       "========================\n"
                       "Valid Elf\n"
                       "========================")
        else:
            logs.error("\n"
                       "========================\n"
                       "File {} is invalid! Make sure it is decrypted.\n"
                       "========================".format(elf))
            os.abort()
    if archs == 'orbis' or archs == 'generic_orbis' :
        elf_header1_result = header.read(0x8)  # save
        header.seek(0x4000, 0)
        elf_header2_result = header.read(0x14)  # save
        if elf_header1_result == orbis_valid_header1 and orbis_valid_header2 == elf_header2_result:
            logs.debug("\n"
                       "========================\n"
                       "Valid Elf\n"
                       "========================")
        else:
            logs.error("\n"
                       "========================\n"
                       "File {} is invalid! Make sure it is a valid dump from AppDumper and Retail Disc/Digital, not Fake Packaged Titles.\n"
                       "========================".format(elf))
            os.abort()
    header.close()

def cloneFile(elf_file, outdate=False):
    if outdate:
        out = os.path.join(os.getcwd(), datetime.now().strftime(
            '{0}-%Y-%m-%d-%H-%M-%S/{0}'.format(os.path.basename(elf_file))))
    else:
        out = os.path.join(os.getcwd(), ('{0}-patched/{0}'.format(os.path.basename(elf_file))))
    # Clone the file
    logs.info('\nSaving file to: {}'.format(out))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copyfile(elf_file, out)
    return out

def loadConfig(elf_file, conf_file, verbose, outdate, ci):
    # Checking desired verbosity level
    if verbose:
        coloredlogs.set_level(logs.DEBUG)

    # Open the config file
    with open(conf_file) as fh:
        read_data = yaml.safe_load(fh)

        for i in range(0, len(read_data)):
            # Run headercheck() depending on run mode
            if ci:
                logs.debug('\nRunning in Buildbot Mode.')
            else:
                logs.debug('\nRunning in User Mode.')
                # Verify the ELF file
                headercheck(read_data[i]['arch'], elf_file)
            # Print Metadata
            logs.info("\n"
                      "=====================\n"
                      "= Game Title    : {}\n"
                      "= Game Version  : {}\n"
                      "= Patch Version : {}\n"
                      "= Patch Name    : {}\n"
                      "= Patch Author  : {}\n"
                      "= Patch Note    : {}\n"
                      "= Patch Enabled : {}\n"
                      "= Architecture  : {}\n"
                      "====================="
                .format(
                read_data[i]['game'], read_data[i]['app_ver'], read_data[i]['patch_ver'], read_data[i]['name'],
                read_data[i]['author'], read_data[i]['note'], read_data[i]['enabled'], read_data[i]['arch']))
            # Clone the ELF file
            out = cloneFile(elf_file, outdate)
            count = 0
            if read_data[i]['enabled'] == False:

                logs.warning('\nPatch: "{}" for "{}" is disabled and will be skipped.'.format(read_data[i]['name'],
                                                                                              read_data[i]['game'], ))
            else:
                ## Load the architecture according to the config
                if read_data[i]['arch'].upper() in arch_dic.keys():
                    architecture = arch_dic.get(read_data[i]['arch'].upper())()
                    # Reading patch list
                    for patch_data in read_data[i]['patch_list']:
                        count += 1
                        logs.info("\nApplying patch: {}".format(count))
                        logs.debug("\n"
                                   "====================\n"
                                   "= Patch Type    : {}\n"
                                   "= Offset (Real) : {}\n"
                                   "= Value         : {}\n"
                                   "= OutFile       : {}\n"
                                   "= Line          : {}\n"
                                   "===================="
                                   .format(patch_data[0], hex(patch_data[1]), patch_data[2], out, count))
                        # Process the patch according to it's architecture
                        final_data = architecture.convertData(patch_data[0], patch_data[1], patch_data[2])
                        patchfile(final_data.get('offset'), final_data.get('value'), out, count)
                else:
                    logs.error("\n{} is not a supported Architecture.".format(read_data[i]['arch']))

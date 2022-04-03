import os
import coloredlogs
import shutil
import logging as logs
import requests
import yaml
from datetime import datetime

from src.archtype.archtypes import Cell, Generic, GenericOrbis, Orbis
from src.prog_ver import program_version

# Easily load different architectures
arch_dic = {
    "CELL": Cell,
    "GENERIC": Generic, # for direct file patch
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

def downloadPatch(url, patch_file):
    file_request = requests.get(url)
    open(patch_file, 'wb').write(file_request.content)
    shutil.unpack_archive(patch_file, '')
    os.remove(patch_file)

def headercheck(archs, elf):
    header = open(elf, "rb")
    cell_valid_header   = b'\x7F\x45\x4C\x46\x02\x02\x01\x66'
    orbis_valid_header1 = b'\x7F\x45\x4C\x46\x02\x01\x01\x09'
    orbis_valid_header2 = b'\x2F\x6C\x69\x62\x65\x78\x65\x63\x2F\x6C\x64\x2D\x65\x6C\x66\x2E\x73\x6F\x2E\x31'
    if archs == 'cell':
        elf_header = header.read(0x8)
        if elf_header == cell_valid_header:
            logs.debug("\n"
                       "========================\n"
                       "Valid Elf\n"
                       "========================")
        else:
            logs.error("\n"
                       "========================\n"
                       "File {} is invalid! Make sure it is decrypted.\n"
                       "Aborting.\n"
                       "========================".format(elf))
            os.abort()
    if archs == 'orbis' or archs == 'generic_orbis':
        elf_header1_result = header.read(0x8)
        header.seek(0x4000, 0)
        elf_header2_result = header.read(0x14)
        if elf_header1_result == orbis_valid_header1 and orbis_valid_header2 == elf_header2_result:
            logs.debug("\n"
                       "========================\n"
                       "Valid Elf\n"
                       "========================")
        else:
            logs.error("\n"
                       "========================\n"
                       "File {} is invalid! Make sure it is a valid dump from Retail Disc/Digital, not Fake Packaged Titles.\n"
                       "Aborting.\n"
                       "========================".format(elf))
            os.abort()
    header.close()

def cloneFile(elf_file, outdate=False, output=None, patched=False):
    if outdate:
        out = os.path.join(os.getcwd(), datetime.now().strftime(
            '{0}-%Y-%m-%d-%H-%M-%S/{0}'.format(os.path.basename(elf_file))))
    elif outdate == False and output == None:
        out = os.path.join(os.getcwd(), ('{0}-patched/{0}'.format(os.path.basename(elf_file))))
    if output:
        out = '{0}/{1}'.format(output, os.path.basename(elf_file))
    # Clone the file
    # Make sure we only save the new file once
    if patched == False:
        logs.info('\nSaving file to: {}'.format(out))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(elf_file, out)
    return out

def loadConfig(elf_file, conf_file, verbose, outdate, outputpath, ci, patch_prompt, download):
    patch_file     = 'patch.zip'
    patch_folder   = 'patch0'
    patch_url      = (f'https://illusion0001.github.io/_patch/{patch_file}')
    patchdir_check = os.path.isdir(patch_folder)
    program_msg    = '\nThanks for using py-patch!\nProgram made by illusion0001, ShadowDog with help from aerosoul and contributors.\nCheckout the Project on Github: https://github.com/illusion0001/py-patcher'
    patched        = False

    if patch_prompt:
        if patchdir_check == True and download == True:
            logs.info('\nExisting patch folder \"{}\" detected, Updating will overwrite existing files.'.format(patch_folder))
            answer = input('Would you like to update? [y/n]: ')
            if not answer or answer[0].lower() != 'y':
                download = False
            else:
                download = True

    if download == True:
        # This will overwrite existing enabled patch files
        # Autogen wen?
        logs.info('\nDownloading Patch database from: {}'.format(patch_url))
        downloadPatch(patch_url, patch_file)
        logs.info('\nDownloaded Patch database.\nPlease open and enable your desired patch file in folder: \"{}\"'.format(patch_folder))
        return

    if elf_file == None or conf_file == None:
        logs.error('\nNo input executable or patch file supplied, aborting.')
        os.abort()

    if download == False:
        logs.info("\nWelcome to py-patch! Version: {}\nOpening patch file: {}".format(program_version, conf_file))
    with open(conf_file) as fh:
        read_data = yaml.safe_load(fh)
        for i in range(0, len(read_data)):
            missing_key  = ''
            arch = read_data[i].get('arch', missing_key)
        # Checking desired verbosity level
        if verbose:
            coloredlogs.set_level(logs.DEBUG)
            missing_key  = 'Unknown String!'
        if ci:
            logs.debug('\nRunning in Buildbot Mode.')
        else:
            logs.debug('\nRunning in User Mode.')
            # Verify file
            headercheck(arch, elf_file)
        # Open config file
        for i in range(0, len(read_data)):
            game         = read_data[i].get('game',      missing_key)
            app_ver      = read_data[i].get('app_ver',   missing_key)
            patch_ver    = read_data[i].get('patch_ver', missing_key)
            name         = read_data[i].get('name',      missing_key)
            patch_author = read_data[i].get('author',    missing_key)
            note         = read_data[i].get('note',      missing_key)
            enabled      = read_data[i].get('enabled',        'True') # Todo: Autogen this
            arch         = read_data[i].get('arch',      missing_key)
            patch_list   = read_data[i]['patch_list']
            # Print Metadata
            logs.info("\n"
                      "========================\n"
                      "= Game Title    : {}\n"
                      "= Game Version  : {}\n"
                      "= Patch Version : {}\n"
                      "= Patch Name    : {}\n"
                      "= Patch Author  : {}\n"
                      "= Patch Note    : {}\n"
                      "= Patch Enabled : {}\n"
                      "= Architecture  : {}\n"
                      "========================"
                .format(
                game, app_ver, patch_ver, name,
                patch_author, note, enabled, arch))
            count = 0
            patch_msg = '\nPatch: "{}" for "{}" ({}) is disabled and will be skipped.'.format(name, game, app_ver)
            if enabled == False:
                logs.warning(patch_msg)
            if patch_prompt:
                answer = input('File to be patched: {}\nConfirmation:\nAre you sure you want to apply this patch? [y/n]: '.format(elf_file))
                if not answer or answer[0].lower() != 'y':
                    patch_msg = '\nPatch: Disabling entry "{}" for "{}" will be skipped.'.format(name, game, app_ver)
                    logs.warning(patch_msg)
                    enabled = False
            if enabled == True:
                out = cloneFile(elf_file, outdate, outputpath, patched)
                ## Load the architecture according to the config
                if arch.upper() in arch_dic.keys():
                    architecture = arch_dic.get(arch.upper())()
                    # Reading patch list
                    for patch_data in patch_list:
                        count += 1
                        logs.info("\nApplying patch: {}".format(count))
                        patch_type  = patch_data[0]
                        patch_addr  = patch_data[1]
                        patch_value = patch_data[2]
                        logs.debug("\n"
                                   "========================\n"
                                   "= Patch Type    : {}\n"
                                   "= Offset (Real) : {}\n"
                                   "= Value         : {}\n"
                                   "= OutFile       : {}\n"
                                   "= Line          : {}\n"
                                   "========================"
                                   .format(patch_type, hex(patch_addr), patch_value, out, count))
                        # Process the patch according to it's architecture
                        final_data = architecture.convertData(patch_type, patch_addr, patch_value)
                        patchfile(final_data.get('offset'), final_data.get('value'), out, count)
                        patched = True
                else:
                    logs.error("\n{} is not a supported Architecture.".format(arch))
    if patched == True:
        logs.info('\nSuccessfully save patched file to: {}'.format(out))
    else:
        logs.info('\nPatches were declined, no changes are made.')
    logs.debug(program_msg)
    logs.info('\nOperations completed, closing program.')

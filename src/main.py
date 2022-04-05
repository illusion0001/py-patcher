import os
import coloredlogs
import shutil
import logging as logs
import requests
import yaml
import questionary
import glob
from datetime import datetime
from pathlib import Path

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

    patch_folder = 'patch0'
    patch_url    = 'https://illusion0001.github.io/_patch/'
    config_dir   = 'config'
    config_gen   = '{}/py-patch-config.yml'.format(config_dir)
    condir_check = os.path.isdir(config_dir)

    logs.info("\nWelcome to py-patch! Version: {}".format(program_version, conf_file))

    if Path(config_gen).is_file() == False:
        if condir_check == False: # if folder doesn't exist
                                  # create it
            os.mkdir(config_dir)
        con_file = open(config_gen, 'w')
        con_gen_data = ("folder_path: \'{}\'\n"
                        "patch_url_base: \'{}\'\n".format(patch_folder, patch_url))
        con_file.write(con_gen_data)
        con_file.close()

    # else:
    with open (config_gen, 'r') as config:
        read_data = yaml.safe_load(config)
        missing_key  = ''
        patch_folder = read_data.get('folder_path',    missing_key)
        patch_url    = read_data.get('patch_url_base', missing_key)

    patch_file       = 'patch.zip'
    patch_url_full   = (f'{patch_url}{patch_file}')
    patchdir_check   = os.path.isdir(patch_folder)
    program_msg      = '\nThanks for using py-patch!\nProgram made by illusion0001, ShadowDog with help from aerosoul and contributors.\nCheckout the Project on Github: https://github.com/illusion0001/py-patcher'
    patched          = False
    patch_ext        = 'yml'
    patch_path       = ('{}/**/*.{}'.format(patch_folder, patch_ext))
    patches_key      = []
    patch_name_key   = []
    FilePick         = 'FilePick: '
    PatchFilePick    = 'PatchFilePick: '
    PatchSelPick     = 'PatchSelectionPick: '
    DownloadSel      = 'DownloadQuestion: '
    glob_yes         = True
    manual_conf_file = conf_file
    patched_state    = False
    reloading        = None

    if patch_prompt:
        if patchdir_check == True and download == True:
            logs.info('\nExisting patch folder \"{}\" detected, Updating will overwrite existing files.'.format(patch_folder))
            download = questionary.confirm("Would you like to update the database?", qmark=DownloadSel).ask()

    if patchdir_check == False:
        logs.info('\nPatch folder \"{}\" not found!'.format(patch_folder))
        download = questionary.confirm("Would you like to download the database?", qmark=DownloadSel).ask()

    if download == True:
        logs.info('\nDownloading Patch database from: {}'.format(patch_url_full))
        downloadPatch(patch_url_full, patch_file)
        logs.info('\nDownloaded Patch database.\nSaved to folder: \"{}\"'.format(patch_folder))

    while glob_yes:
        if elf_file == None:
            elf_file = questionary.path("What is the path for the executable file?", qmark=FilePick).ask()
            if elf_file == None or elf_file == '':
                logs.error('\nNo file selected!')
                return
            else:
                logs.info('\nSelected executable file: {}'.format(elf_file))

        if elf_file:
            patches_key = []
            reloading = False
            if manual_conf_file:
                logs.info('\nManual patch file: {}'.format(manual_conf_file))
                conf_file = manual_conf_file
                glob_yes = False
            else:
                conf_file_list = 'Pick file from folder: {}'.format(patch_folder)
                conf_file_type = 'Type in patch file manually'
                conf_file_sel = questionary.select("Select patch file:", qmark=PatchFilePick, choices=[conf_file_list, conf_file_type]).ask()

                if conf_file_sel == conf_file_list:
                    # ask user to pick a file
                    logs.info('\nGetting file listing from folder: {}'.format(patch_folder))
                    # Get all patch files within patch0 folder
                    for conf_file in glob.glob(patch_path, recursive=True):
                        patches_key.append(conf_file)
                        glob_yes = True
                    conf_file = questionary.select("Select patch file:", qmark=PatchFilePick, choices=patches_key).ask()
                elif conf_file_sel == conf_file_type:
                    conf_file = questionary.path("What is the path for the patch file?", qmark=FilePick).ask()

                if conf_file == None or conf_file == '':
                    logs.error('\nNo patch file selected!')
                    return
                else:
                    logs.info('\nSelected patch file: {}'.format(conf_file))
            patched_state = True

            while patched_state == True:
                # open patch file
                with open(conf_file) as fh:
                    patch_count    = 0 # reset number of patches
                    patch_name_key = []
                    logs.info("\nOpened patch file: {}".format(conf_file))
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
                        patch_text = 'patch file: {}'.format(conf_file)
                        if reloading:
                            logs.info('\nReloaded {}'.format(patch_text))
                        else:
                            logs.info('\nLoaded {}'.format(patch_text))
                    # Open config file
                    for i in range(0, len(read_data)):
                        # only fetch the keys we need
                        game             = read_data[i].get('game',      missing_key)
                        app_ver          = read_data[i].get('app_ver',   missing_key)
                        name             = read_data[i].get('name',      missing_key)
                        patch_list       = read_data[i]['patch_list']
                        count            = 0
                        patch_count     += 1
                        patch_title      = 'Patch name:'
                        game_title       = 'Game title:'
                        game_ver_title   = 'Game version:'
                        name_key = ('{} {}\n     {} {}\n     {} {}'.format(patch_title, name, game_title, game, game_ver_title ,app_ver))
                        patch_name_key.append(name_key)
                    logs.info('\nNumber of patches available: {}'.format(patch_count))
                    name = questionary.checkbox("Select the patch you want to apply: (Ctrl+C to Cancel)", qmark=PatchSelPick, choices=patch_name_key).ask()
                    if name == '' or name == [] or name == None:
                        patched = False
                        enabled = False
                    elif name != '' or name != []:
                        for name1 in name:
                            for i in range(0, len(read_data)):
                                game_new       = read_data[i].get('game',      missing_key)
                                app_ver_new    = read_data[i].get('app_ver',   missing_key)
                                patch_ver      = read_data[i].get('patch_ver', missing_key)
                                name_new       = read_data[i].get('name',      missing_key)
                                patch_author   = read_data[i].get('author',    missing_key)
                                note           = read_data[i].get('note',      missing_key)
                                arch           = read_data[i].get('arch',      missing_key)
                                patch_list_new = read_data[i]['patch_list']
                                name_key_new = ('{} {}\n     {} {}\n     {} {}'.format(patch_title, name_new, game_title, game_new, game_ver_title ,app_ver_new))
                                if name1 == name_key_new:
                                    patch_list = patch_list_new
                                    logs.info("\n"
                                            "========================\n"
                                            "= Game Title    : {}\n"
                                            "= Game Version  : {}\n"
                                            "= Patch Version : {}\n"
                                            "= Patch Name    : {}\n"
                                            "= Patch Author  : {}\n"
                                            "= Patch Note    : {}\n"
                                            "= Architecture  : {}\n"
                                            "========================"
                                        .format(
                                        game_new, app_ver_new, patch_ver, name_new,
                                        patch_author, note, arch))
                                    enabled = True
                            if enabled == True:
                                out = cloneFile(elf_file, outdate, outputpath, patched)
                                # Load the architecture according to the config
                                if arch.upper() in arch_dic.keys():
                                    architecture = arch_dic.get(arch.upper())()
                                    # Reading patch list
                                    for patch_data in patch_list:
                                        count += 1
                                        logs.info("\nApplying patch: {}".format(count))
                                        patch_type  = patch_data[0]
                                        patch_addr  = patch_data[1]
                                        patch_value = patch_data[2]
                                        # Process the patch according to it's architecture
                                        final_data = architecture.convertData(patch_type, patch_addr, patch_value)
                                        patchfile(final_data.get('offset'), final_data.get('value'), out, count)
                                        patched = True
                                        glob_yes = False
                                        patch_name_key = []
                                else:
                                    logs.error("\n{} is not a supported Architecture.".format(arch))
                    if patched == True:
                        logs.info('\nSuccessfully save patched file to: {}'.format(out))
                        patched_state = False
                    else:
                        logs.info('\nPatches were declined, no changes are made.')
                    logs.debug(program_msg)

                restart_full     = 'Return to executable file select.'
                restart_partial  = 'Return to patch file select.'
                restart_partial2 = 'Return to patch entry select.'
                exit_program     = 'Exit the program.'
                closing_prog     = '\nOperations completed, closing program.'
                restart = questionary.select("Would you like to apply more patches?", choices=[restart_full, restart_partial, restart_partial2,exit_program]).ask()
                if restart == restart_full:
                    patched          = False
                    manual_conf_file = None
                    conf_file        = None
                    elf_file         = None
                    loadConfig(elf_file, conf_file, verbose, outdate, outputpath, ci, patch_prompt, download)
                elif restart == restart_partial:
                    manual_conf_file = None
                    reloading        = True
                    glob_yes         = True
                    patched          = False
                    logs.debug('Glob: {}'.format(glob_yes))
                elif restart == restart_partial2:
                    manual_conf_file = None
                    reloading        = True
                    patched_state    = True
                elif restart == exit_program:
                    logs.info(closing_prog)
                    return
                else:
                    logs.info(closing_prog)
                    return

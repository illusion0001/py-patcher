import argparse
import base64
import os
import coloredlogs
import shutil
import logging
import yaml
from datetime import datetime

def patchfile(type, offset_pre, hexadecimal_string, out, count):
    byte_array = bytearray.fromhex(hexadecimal_string)
    path = out
    offset_post = offset_pre  # need to be declared before use
    logs.debug('\nPatch type: {}'.format(type))
    with open(path, 'r+b') as f:
        # normal path
        f.seek(offset_post, 0)
        # if iscell == True and isorbis == True:
        #     logs.error("\n"
        #                "==============================================================\n"
        #                "ERROR: Cannot use two architecture at the same time, aborting!\n"
        #                "==============================================================")
        #     os.abort()
        # # cell path, scrap this?
        # if iscell == True:
        #     offset_post = offset_pre - 0x10000
        #     f.seek(offset_post, 0)
        # # orbis path, scrap this?
        # elif isorbis == True:
        #     offset_post = offset_pre - 0x3FC000 # disabled aslr addr - file addr
        #     f.seek(offset_post, 0)
        f.write(byte_array)
        logs.info(
            "\nApplied Patch Line {} in file: {}".format(count, out))

def loadConfig(elf_file, conf_file, verbose, outdate):
    with open(conf_file) as fh:
        read_data = yaml.safe_load(fh)
        input = elf_file
        if outdate == True:
          out = os.path.join(os.getcwd(), datetime.now().strftime(
              '{0}-%Y-%m-%d-%H-%M-%S/{0}'.format(os.path.basename(input))))
        out = os.path.join(os.getcwd(), ('{0}-patched/{0}'.format(os.path.basename(input))))
        logs.info('\nSaving file to: {}'.format(out))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copyfile(input, out)
        for i in range(0, len(read_data)):
            # Checking desired verbosity level
            if verbose == True:
                coloredlogs.set_level(logging.DEBUG)
            # Print Metadata
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
            count = 0

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
                            "= OutFile       : {}\n"
                            "= Line          : {}\n"
                            "====================".format(patch_data[0], hex(patch_data[1]), patch_data[2],
                                                            out, count))
                    patchfile(patch_data[0], patch_data[1], patch_data[2], out, count)

if __name__ == "__main__":
    # Basic Logs Config
    logging.basicConfig()
    logs = logging.getLogger(__name__)
    coloredlogs.install(level=logging.INFO, logger=logs)
    # Basic CLI config
    parser = argparse.ArgumentParser(
        prog="patcher-yml.py",
        description=base64.b64decode(
            "ICAgLi0tLS0tLS0tLS0tLS0uICAgICAgIC4gICAgLiAgICogICAgICAgKgogIC9"
            "fL18vXy9fL18vXy9fLyBcICAgICAgICAgKiAgICAgICAuICAgKSAgICAuCiAvL18"
            "vXy9fL18vXy9fLy8gXyBcIF9fICAgICAgICAgIC4gICAgICAgIC4KL18vXy9fL1"
            "8vXy9fL18vfC8gXC4nIC5gLW8KIHwgICAgICAgICAgICAgfHwtJygvICwtLScKIH"
            "wgICAgICAgICAgICAgfHwgIF8gfAogfCAgICAgICAgICAgICB8fCcnIHx8ICAgI"
            "CAgICAgICBNYWRlIGJ5OgogfF9fX19fX19fX19fX198fCB8X3xMICAgICAgICAgI"
            "CBpbGx1c2lvbgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFNoYWRv"
            "d0RvZwogICAgICAgICAgICAgICAgICAgICBBdmF0YXI6IENsb3VkIFN0cmlmZQog"
            "ICAgICAgICAgICgoKCUjIyUoLygoKCgoIyUlICAgICAgICAgICAgICAgICAKICA"
            "gICAgICAgICAlKCgvIy8lJSMvKCUoIygmJSUlJSAgICAgICAgICAgICAgCiAgICA"
            "gICAgICAgIC8vKCUmJSMlLyUvJSUmQEBAQEAmJiAgICAgICAgICAgIAogICAgIC"
            "AgICAoKC8qLyMlIyUlJiMvLy8vJiZAQCYmJiUmLiAgICAgICAgICAKICAgICAgIC"
            "AgIC4vLyMlIy8jJSojLy8oIyglJiYmJiYmJiYmICAgICAgICAgCiAgICAgICAgI"
            "C8jIyovKCglIyUjIygvIyUmJSZAJiUlJiYmJiYgICAgICAgIAogICAgICAgLyUvL"
            "yovKCMjIyglJSUmJiUvKCYmJUAmJiYmJiAgICAgICAgICAKICAgICAgICAvLyoo"
            "LyUqKioqJSMlKC8uLi8sKiUmJiUlIyYgICAgICAgICAgCiAgICAgICAoIC8gKigo"
            "KioqKiovQCYmJSUmQCMlKCUmLyAgICAgICAgICAgIAogICAgICAoICAgICAoKC8"
            "vLy8qLyYmJiYmJiYmJSUmJiMsICAgICAgICAgICAKICAgICAgICAgICAgICggLiw"
            "vLyovJiYmJiYmJiMmIy4uLCAgICAgICAgICAgCiAgICAgICAgICAgICAvICAgKi"
            "oqKi8jJiYmJiMuJi4uLi4sICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIC"
            "4vIyYmLi4uLi8uLiAuLi4uLi4gICAgLCAKICAgICAgICAgICAgICAsIC4gICAgI"
            "CAuICAgLiAgICAgLiAgLiwsLiAuLi4uCiAgICAgICAgICAqKiogICAgICAgICAgI"
            "CAgICAgICAgICosLC4uLi4uLi4uLgogICAgICAgICAqKiouICAgICAgICAgICAg"
            "ICAgICAgKi4uLi4uLi4uLi4uLiwKICAgICAgICAqKiAuICAgICAgICAgICAgICAg"
            "Li4uICAuLi4qLi4uLi4uLCwsCiAgICAgICAgKiAuICAgICAgICAgICAgICAgIC4"
            "uLiAgLi4sIC8uLi4uLi4uLAo=").decode('utf-8')
        , formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-f',
                        '--file',
                        required=True,
                        help='The ELF file to be patched.')
    parser.add_argument('-c',
                        '--config',
                        required=True,
                        help='The configuration file.')
    parser.add_argument('-v',
                        '--verbose',
                        required=False,
                        action="store_true",
                        help='Enable Verbose Mode.')
    parser.add_argument('-od',
                        '--outputdate',
                        required=False,
                        action="store_true",
                        help='Append date and time to output directory.')
    args = parser.parse_args()

    # Load the config file, and patch the ELF file
    loadConfig(args.file, args.config, args.verbose, args.outputdate)

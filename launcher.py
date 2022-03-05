from src.main import loadConfig
import argparse
import base64
import logging as logs
import coloredlogs

if __name__ == "__main__":
    # Basic Logs Config
    logs.basicConfig()
    coloredlogs.install(level=logs.INFO)
    # Basic CLI config
    parser = argparse.ArgumentParser(
        prog="launcher.py",
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
    parser.add_argument('-ci',
                        '--cibuild',
                        required=False,
                        action="store_true",
                        help='For running tests on buildbot.')
    args = parser.parse_args()

    # Load the config file, and patch the ELF file
    loadConfig(args.file, args.config, args.verbose, args.outputdate, args.cibuild)

"""
---------------
+ spritesplit +
---------------
Join image files into a single sprite map
    spritesplit [-h] [-v] [[UNDER_CONSTRUCTION]]
options:
    -h, --help      show this help message and exit
    -v, --version   show program version information and exit
    [[UNDER_CONSTRUCTION]]
"""
import sys

from . import spritejoin
from .version import __version__


def main():
    """Deploy program given on command line."""
    name_to_function = {
        'spritejoin': spritejoin.main,
    }
    try:
        if sys.argv[1] in ['-v', '--version']:
            print(f'spritejoin {__version__}')
            sys.exit(0)
        elif sys.argv[1] in ['-h', '--help']:
            print(__doc__.strip())
            sys.exit(0)
    except IndexError:  # Only program name was given
        sys.stderr.write('Usage: spritesplit [-h] [-v] [[UNDER_CONSTRUCTION]]\n')
        sys.exit(0)

    program_name = sys.argv[0].split('/')[-1]
    arguments = sys.argv[1:]
    try:
        name_to_function[program_name](arguments)
    except KeyError as exc:
        raise ValueError("Invalid program entered") from exc


if __name__ == '__main__':
    main()

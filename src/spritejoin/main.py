#! /usr/bin/env python3
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
# mypy: allow-redefinition
import sys

try:
    from . import spritejoin
    from .version import __version__
    STANDALONE = False
except ImportError:
    import spritejoin  # type: ignore [no-redef]
    STANDALONE = True

def main() -> None:
    """Deploy program given on command line."""
    name_to_function = {
        'spritejoin': spritejoin.main,
    }
    #try:
    #    if sys.argv[1] in ['-v', '--version']:
    #        print(f'spritejoin {__version__}')
    #        sys.exit(0)
    #    elif sys.argv[1] in ['-h', '--help']:
    #        print(__doc__.strip())
    #        sys.exit(0)
    #except IndexError:  # Only program name was given
    #    sys.stderr.write('Usage: spritesplit [-h] [-v] [[UNDER_CONSTRUCTION]]\n')
    #    sys.exit(0)
    #if len(sys.argv) == 1:  # Only program name was given
    #    sys.stderr.write('Usage: spritesplit [-h] [-v] [[UNDER_CONSTRUCTION]]\n')
    #    sys.exit(0)

    program_name = sys.argv[0].split('/')[-1]
    arguments = sys.argv[1:]
    try:
        name_to_function[program_name](arguments, __version__)
    except KeyError as exc:
        if STANDALONE:
            name_to_function['spritejoin'](arguments, 'standalone')
            return
        raise ValueError("Invalid program entered") from exc


if __name__ == '__main__':
    main()

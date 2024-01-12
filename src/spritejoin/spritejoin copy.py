#! /usr/bin/env python3
from __future__ import annotations
import sys
import os
import argparse
import math

from PIL import Image


class Vector(tuple):
    def __init__(self, values: tuple[int | float, int | float] = (0, 0)) -> None:
        super().__init__()
        self.x = values[0]
        self.y = values[1]
        self.values = (self.x, self.y)

    def add_vector(self, vector: Vector):
        vector = Vector(vector)
        self.x += vector.x
        self.y += vector.y


def join_images(
        image_paths: set[str],
        directory: str | None = None,
        exclusions: set[str] = set(),
        output_path: str = '-') -> None:
    """Join images and output sprite sheet."""
    image_paths = set(image_paths)
    exclusions = set(exclusions)
    if directory is not None:
        with os.scandir(directory) as directory_list:
            image_paths |= set(entry.path for entry in directory_list if entry.is_file())
    image_paths -= exclusions

    total_size = (0, 0)
    image_sizes = {}
    for image_path in image_paths:
        with Image.open(image_path) as image:
            image_sizes.update({image_path: image.size})
            total_size = (total_size[0] + image.size[0], total_size[1] + image.size[1])
    n_images = len(image_sizes)
    total_area = math.prod(total_size)
    optimal_area = total_area / n_images
    optimal_area_sqrt = math.sqrt(optimal_area)
    
    print(f'File number: {n_images}')
    print(f'Total x and y: {total_size}')
    print(f'Total area: {total_area}')
    print(f'Optimal area: {optimal_area} (Sqrt: {optimal_area_sqrt})')


def get_file_names(file_paths: set[str]) -> set[str]:
    return set(os.path.basename(i) for i in file_paths)


def main(arguments: list[str] | None = None, version: str = 'standalone') -> None:
    """Parse arguments and call function

    Args:
        arguments (list[str] | None, optional): arguments to pass to argparser. Parses command line
        arguments if None. Defaults to None.
        version (str, optional): version number. Defaults to 'standalone'.
    """
    parser = argparse.ArgumentParser(prog='spritejoin',
                                     description='Join image files into a single sprite sheet.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')

    input_options = parser.add_argument_group('Input options')
    input_options.add_argument('infiles', nargs='*',
                               help='Files to join. Will join in addition to the files '+
                               'found in `-d`, if it is provided. Required if `-d` is not provided')
    input_options.add_argument('-d', '--directory',
                               help='Directory containing files to join. Takes all image files'+
                               'found in the directory. Required if no `infiles` are provided.')
    input_options.add_argument('-e', '--exclude', nargs='+', default=[],
                               help='Path to files to exclude from joining that are given in '
                               '`infiles` or found in `-d`.')

    output_options = parser.add_argument_group('Output options')
    output_options.add_argument('-o', '--output', default='-',
                                help='Path for generated sprite sheet. Writes to standard out '+
                                "if not provided or if '-' is provided.")

    args = parser.parse_args(arguments)
    if args.infiles == [] and args.directory is None:
        parser.print_usage()
        sys.stderr.write('Must provide files using either `infiles` or `-d`.\n')
        sys.exit(0)
    if args.directory is not None:
        args.directory = args.directory.rstrip('/')
    join_images(args.infiles, args.directory, args.exclude, args.output)


if __name__ == '__main__':
    main()

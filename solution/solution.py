from sys import argv
from argparse import ArgumentParser
from argparse import Namespace
from os import environ
from os import getcwd
import os
import json


PROGRAM_NAME = 'program'
VERSION = '1.0.0'
OUTPUT_ENV = 'TARGET_DIRECTORY'
INPUT_ENV = 'SOURCE_DIRECTORY'

DATE = 'date'


def get_target(filename: str) -> str:
    index = filename.find('-') + 1
    new_name = filename[index:]
    return new_name


def get_file_name(inputted: str, env_name: str) -> str:
    if inputted is not None:
        return inputted
    name = environ.get(env_name)
    if name is not None:
        return name

    return getcwd()


def parse_input() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help="Directory, from which is input taken.")
    parser.add_argument('-o', '--output', help="Directory, where to put output.")
    parser.add_argument('--version', '-v', action='store_true', help="Prints the version of the program.")
    parser.add_argument('--write', '-w', action='store_true', help="Makes the operation for real.")
    return parser.parse_args()


def main() -> int:
    args = parse_input()
    if args.version:
        print(PROGRAM_NAME, VERSION)
        return 0

    input_dir = get_file_name(args.input, INPUT_ENV)
    output_dir = get_file_name(args.output, OUTPUT_ENV)
    is_writing = args.write

    files = os.listdir(input_dir)
    print(f'Processing {len(files)} files...')
    for filename in files:
        directory = {}
        file_path = str(os.path.join(input_dir, filename))
        directory['source'] = file_path
        output_name = str(os.path.join(output_dir, get_target(filename)))
        directory['target'] = output_name
        print(directory)

    return 0


if __name__ == "__main__":
    main()
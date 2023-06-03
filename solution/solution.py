from sys import argv
from argparse import ArgumentParser
from os import environ
from os import getcwd


PROGRAM_NAME = 'program'
VERSION = '1.0.0'
OUTPUT_ENV = 'TARGET_DIRECTORY'
INPUT_ENV = 'SOURCE_DIRECTORY'


def get_file_name(inputted, env_name):
    if inputted is not None:
        return inputted
    name = environ.get(env_name)
    if name is not None:
        return name

    return getcwd()


def parse_input():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', help="Directory, from which is input taken.")
    parser.add_argument('-o', '--output', help="Directory, where to put output.")
    parser.add_argument('--version', '-v', action='store_true', help="Prints the version of the program.")
    parser.add_argument('--write', '-w', action='store_true', help="Makes the operation for real.")
    return parser.parse_args()


def main():
    args = parse_input()
    if args.version:
        print(PROGRAM_NAME, VERSION)
        return 0

    input_name = get_file_name(args.input, INPUT_ENV)
    output_name = get_file_name(args.output, OUTPUT_ENV)


    return 0

if __name__ == "__main__":
    main()
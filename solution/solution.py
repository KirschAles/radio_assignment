from sys import argv
from argparse import ArgumentParser


PROGRAM_NAME = 'program'
VERSION = '1.0.0'


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
    return 0

if __name__ == "__main__":
    main()
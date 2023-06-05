from sys import argv
from argparse import ArgumentParser
from argparse import Namespace
from os import environ
from os import getcwd
import os
import json
from datetime import date


PROGRAM_NAME = 'program'
VERSION = '1.0.0'
OUTPUT_ENV = 'TARGET_DIRECTORY'
INPUT_ENV = 'SOURCE_DIRECTORY'

DATE = 'date'

WEEK_PREPOSITION = 'W'
JSON = '.json'


def print_dir(directory: dir) -> None:
    print("{'source': ", end='')
    print(f"'{directory['source']}', ", end='')
    print(f"'target': '{directory['target']}'", end='')
    print('}')


def is_json(filename: str) -> bool:
    last_dost = filename.rfind('.')
    return filename[last_dost:] == JSON


def get_date_from_filename(filename: str) -> date:
    index_end = filename.find('_')
    return date.fromisoformat(filename[:index_end])


def get_target(filename: str) -> str:
    index = filename.find('-') + 1
    new_name = filename[index:]
    date1 = get_date_from_filename(filename)
    year = str(date1.year)
    week = WEEK_PREPOSITION + str(date1.isocalendar().week).zfill(2)
    return os.path.join(year, week, new_name)


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


def do_dates_match(filename: str, source_path: str) -> bool:
    index_date = filename.find('_')
    date1 = date.fromisoformat(filename[:index_date])
    with open(source_path, 'r') as file:
        source_info = json.load(file)
        date2 = date.fromisoformat(source_info['date'])
    return date1 == date2


def move_file(directory: dir, is_writing: bool) -> None:
    if not is_writing:
        return


def main() -> int:
    args = parse_input()
    if args.version:
        print(PROGRAM_NAME, VERSION)
        return 0

    input_dir = get_file_name(args.input, INPUT_ENV)
    output_dir = get_file_name(args.output, OUTPUT_ENV)
    is_writing = args.write

    files = [x for x in os.listdir(input_dir) if is_json(x)]
    print(f'Processing {len(files)} files...')
    processed_files = 0
    for filename in files:
        directory = {}
        source_path = str(os.path.join(input_dir, filename))
        directory['source'] = source_path
        target_path = str(os.path.join(output_dir, get_target(filename)))
        directory['target'] = target_path
        print_dir(directory)

        if do_dates_match(filename, source_path):
            processed_files += 1
            move_file(directory, is_writing)
        else:
            print(f"Moving of file {source_path} failed.")

    processed_all = processed_files == len(files)
    first_word = 'Success'
    if not processed_all:
        first_word = 'Failure'

    print(f"{first_word}: processed {processed_files}/{len(files)} files.")
    return processed_all


if __name__ == "__main__":
    main()
import sys
from argparse import ArgumentParser
from argparse import Namespace
from os import environ
from os import getcwd
import os
import json
from datetime import date
import re


PROGRAM_NAME = 'program'
VERSION = '1.0.0'
OUTPUT_ENV = 'TARGET_DIRECTORY'
INPUT_ENV = 'SOURCE_DIRECTORY'

DATE = 'date'

WEEK_PREPOSITION = 'W'
JSON = '.json'

UNKNOWN = '??'
FILENAME_PATTERN = r"^\d{4}-\d{2}-\d{2}_\d{1}\.json$"


def print_error(msg: str) -> None:
    print(msg, file=sys.stderr)


def print_dir(directory: dir) -> None:
    print("{'source': ", end='')
    print(f"'{directory['source']}', ", end='')
    print(f"'target': '{directory['target']}'", end='')
    print('}')


def is_json(file_path: str) -> bool:
    try:
        with open(file_path) as f:
            directory = json.load(f)
    except json.JSONDecodeError:
        return False
    return True


def get_date_from_filename(filename: str) -> date:
    index_end = filename.find('_')
    return date.fromisoformat(filename[:index_end])


def get_target(filename: str) -> str:
    index = filename.find('-') + 1
    # exception here is impossible, at worst would get filename[0:]
    new_name = filename[index:]
    try:
        date1 = get_date_from_filename(filename)
        year = str(date1.year)
        week = WEEK_PREPOSITION + str(date1.isocalendar().week).zfill(2)
    # using this, to avoid dispersing error handling to several places
    except ValueError:
        year = UNKNOWN
        week = UNKNOWN
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

    try:
        with open(source_path, 'r') as file:
            source_info = json.load(file)
            date2 = date.fromisoformat(source_info['date'])
    except IOError:
        return False
    except json.JSONDecodeError:
        return False
    except ValueError:
        return False
    return date1 == date2


def reading_failed(path: str) -> None:
    print_error(f"Couldn't read from file {path}.")


def writing_failed(path: str) -> None:
    print_error(f"Couldn't write to file {path}.")


def move_file(directory: dir, is_writing: bool) -> bool:
    if not is_writing:
        return True
    data = None
    try:
        with open(directory['source'], 'r') as file:
            data = file.read()
    except IOError:
        reading_failed(directory['source'])
        return False
    if data is None:
        reading_failed(directory['source'])
        return False

    try:
        os.makedirs(os.path.dirname(directory['target']), exist_ok=True)
        with open(directory['target'], 'w') as file:
            file.write(data)
    except (IOError, OSError):
        writing_failed(directory['target'])
        return False

    try:
        os.remove(directory['source'])
    except PermissionError:
        print_error(f"File {directory['source']} couldn't be removed.")
        # transaction failed, roll it back
        os.remove(directory['target'])
        return False
    
    return True


def is_filename_valid(filename: str) -> bool:
    return not re.match(FILENAME_PATTERN, filename) is None


def can_access_file(file_path: str) -> bool:
    try:
        with open(file_path, 'r'):
            pass
    except IOError:
        return False
    return True


def can_process_file(source_path: str, filename: str) -> bool:
    if not is_filename_valid(filename):
        print_error(f"Filename {filename} of file {source_path} is not valid.")
        return False
    try:
        date_filename = get_date_from_filename(filename)
    except ValueError:
        print_error(f"Date from filename {filename} of file {source_path} is not valid.")
        return False

    try:
        with open(source_path, 'r') as file:
            json_info = json.load(file)
            date_json = date.fromisoformat(json_info['date'])
            if date_json != date_filename:
                print_error(f"Date from filename {date_filename} and date from json {date_json} " +\
                            f"of file {source_path} do not match.")
                return False
            return True

    except IOError:
        print_error(f"File {source_path} couldn't be opened.")
        return False
    except json.JSONDecodeError:
        print_error(f"File {source_path} is not valid JSON file.")
        return False


def main() -> int:
    args = parse_input()
    if args.version:
        print(PROGRAM_NAME, VERSION)
        return 0

    input_dir = get_file_name(args.input, INPUT_ENV)
    output_dir = get_file_name(args.output, OUTPUT_ENV)
    is_writing = args.write

    files = os.listdir(input_dir)
    print_error(f'Processing {len(files)} files...')
    processed_files = 0
    for filename in files:
        directory = {}
        source_path = str(os.path.join(input_dir, filename))
        directory['source'] = source_path
        target_path = str(os.path.join(output_dir, get_target(filename)))
        directory['target'] = target_path
        print_dir(directory)

        if can_process_file(source_path, filename):
            processed_files += move_file(directory, is_writing)

    processed_all = processed_files == len(files)
    first_word = 'Success'
    if not processed_all:
        first_word = 'Failure'

    print_error(f"{first_word}: processed {processed_files}/{len(files)} files.")
    return processed_all


if __name__ == "__main__":
    main()
"""Command line interface."""
import argparse
import subprocess
from os.path import exists
from src.backend.jackalify import jackalify


def is_valid_file(parser: argparse.ArgumentParser, arg: str) -> str:
    """Check if file exists.

    :param parser: Argparse parser object.
    :type parser: argparse.ArgumentParser
    :param arg: Argument containing path po file.
    :type arg: str
    :return: Path to file if it exists.
    :rtype: str
    """
    if not exists(arg):
        parser.error(f"The file {arg} does not exist!")
    else:
        return arg


parser = argparse.ArgumentParser(description='Jackalifying algorithm')
parser.add_argument(
    '-w', '--web',
    action='store_true',
    help='Run fastapi server interface'
)
parser.add_argument(
    '-g', '--gif',
    action='store_true',
    help='Create jackalified gif instead of picture'
)
parser.add_argument(
    'input_path',
    nargs='?',
    action='store',
    help='Picture you want to jackalify',
    type=lambda x: is_valid_file(parser, x)
)
parser.add_argument(
    '-o', '--output',
    action='store',
    dest='output_path',
    help='Path to save jackalified instance'
)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.web:
        if args.gif or args.input_path or args.input_path:
            print("-w must be a single argument")
        else:
            subprocess.run(["python", "src/fastapi/main.py"])
    elif args.input_path:
        if args.output_path:
            if args.gif:
                jackalify(args.input_path, video_path=args.output_path)
            else:
                jackalify(args.input_path, out_image_path=args.output_path)
        else:
            if args.gif:
                jackalify(args.input_path, video_path=args.input_path)
            else:
                jackalify(args.input_path, out_image_path=args.input_path)
    else:
        parser.error("No input path given!")

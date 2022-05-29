"""Command line interface."""
import argparse
import os
import subprocess
import sys

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
    path, extention = os.path.splitext(arg)
    if not os.path.exists(arg):
        parser.error(f"The file {arg} does not exist!")
    elif extention.lower() not in ['.png', '.jpg', '.jpeg']:
        parser.error(f"Wrong file extension '{extention}'! Try '.png', '.jpg', or '.jpeg' file!")
    else:
        return arg


parser = argparse.ArgumentParser(description='Jackalifying algorithm')
parser.add_argument(
    '-w', '--web',
    action='store_true',
    help='run fastapi server interface'
)
parser.add_argument(
    '-g', '--gif',
    action='store_true',
    help='create jackalified gif instead of picture'
)
parser.add_argument(
    'input_path',
    nargs='?',
    action='store',
    help='picture you want to jackalify',
    type=lambda x: is_valid_file(parser, x)
)
parser.add_argument(
    '-o', '--output',
    action='store',
    dest='output_path',
    help='path to save jackalified instance',
)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.web:
        if len(sys.argv) > 2:
            parser.error("-w must be a single argument!")
        else:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src", "fastapi", "main.py"))
            subprocess.run(["python", script_path])
    elif args.input_path:
        if args.output_path:
            if args.input_path == args.output_path:
                if args.gif:
                    parser.error("Output file shouldn't be gif!")
                path, extention = os.path.splitext(args.output_path)
                args.output_path = f"{path}_jackalified{extention}"
            if args.gif:
                if not args.output_path.lower().endswith(".gif"):
                    parser.error(f"Output name should end with '.gif'!")
                jackalify(args.input_path, video_path=args.output_path)
            else:
                if not args.output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    parser.error(f"Output name should end with '.png', '.jpg' or '.jpeg'!")
                jackalify(args.input_path, out_image_path=args.output_path)
        else:
            path, extention = os.path.splitext(args.input_path)
            if args.gif:
                output_path = f"{path}_jackalified.gif"
                jackalify(args.input_path, video_path=output_path)
            else:
                output_path = f"{path}_jackalified{extention}"
                jackalify(args.input_path, out_image_path=output_path)
    else:
        parser.error("No input path given!")

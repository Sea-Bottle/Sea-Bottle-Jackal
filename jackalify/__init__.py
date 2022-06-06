"""Jackalify module."""

import argparse
import os
import subprocess
import sys
import gettext

from jackalify.jackal import jackalify

project_dir = os.path.dirname(__file__)
translation = gettext.translation('jackalify', localedir=os.path.join(project_dir, 'locales'), languages=['en', 'ru'])
_ = translation.gettext


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
        parser.error(str.format(_("The file {} does not exist!"), arg))
    elif extention.lower() not in ['.png', '.jpg', '.jpeg']:
        parser.error(str.format(_("Wrong file extension '{}'! Try '.png', '.jpg', or '.jpeg' file!"), extention))
    else:
        return arg


def main():
    """CLI functionality."""
    parser = argparse.ArgumentParser(description=_('Jackalifying algorithm'))
    parser.add_argument(
        '-w', '--web',
        action='store_true',
        help=_('run fastapi server interface')
    )
    parser.add_argument(
        '-g', '--gif',
        action='store_true',
        help=_("create jackalified gif instead of picture")
    )
    parser.add_argument(
        'input_path',
        nargs='?',
        action='store',
        help=_('picture you want to jackalify'),
        type=lambda x: is_valid_file(parser, x)
    )
    parser.add_argument(
        '-o', '--output',
        action='store',
        dest='output_path',
        help=_('path to save jackalified instance'),
    )
    args = parser.parse_args()
    if args.web:
        if len(sys.argv) > 2:
            parser.error(_("-w must be a single argument!"))
        else:
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))
            subprocess.run(["python", script_path])
    elif args.input_path:
        if args.output_path:
            if args.input_path == args.output_path:
                if args.gif:
                    parser.error(_("Output file shouldn't be gif!"))
                path, extention = os.path.splitext(args.output_path)
                args.output_path = f"{path}_jackalified{extention}"
            if args.gif:
                if not args.output_path.lower().endswith(".gif"):
                    parser.error(_("Output name should end with '.gif'!"))
                jackalify(args.input_path, video_path=args.output_path)
            else:
                if not args.output_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    parser.error(_("Output name should end with '.png', '.jpg' or '.jpeg'!"))
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
        parser.error(_("No input path given!"))

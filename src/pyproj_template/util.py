"""util.py, module

utility for notify_ip module
"""
from argparse import ArgumentParser
from pyproj_template import VERSION
import sys
import git


def get_args():
    """get_args, function

    get command-line arguments

    Returns:
        NameSpace: parser.parse_args() returns

    Note:
        No note

    """
    parser = ArgumentParser(description='IP notify tool')
    parser.add_argument('--version', default=False, action="store_true",
                        help='show version')
    parser.add_argument('--out', type=str, default="./py_template",
                        help='output folder')
    return parser


def main():
    """main, function

    main function

    Args:
        No Argument

    Returns:
        None:
    """
    parser = get_args()
    args = parser.parse_args()
    if args.version is True:
        print(VERSION)

    url = 'git@github.com:CodeSpaceTeam-Alt/pyproj_template.git'
    git.Repo.clone_from(url, args.out)


if __name__ == "__main__":
    sys.exit(main())

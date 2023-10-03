#!/usr/bin/python3

import subprocess, argparse
from mutagen._file import File as AudioFile

__version__ = 0.1

# TODO: redo all of this shit...

parser = argparse.ArgumentParser(prog='yt-music',
    description="Downloads YouTube videos as music with overwritable metadata.")
parser.add_argument('links',
                    nargs="+",
                    help='Space-separated links to download')
parser.add_argument('-a', '--append',
                    metavar='K:V',
                    action='append',
                    dest='metadata',
                    help='Append metadata in KEY:VALUE format. Repeatable.')
parser.add_argument('-v', '--version',
                    action='version',
                    version=f"%(prog)s {__version__}")
args = parser.parse_args()

print(args)

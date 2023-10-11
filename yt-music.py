#!/usr/bin/python3

# NOTE: possibly use https://pypi.org/project/rich-argparse/
# TODO: turn every audio file's artist tag into a proper array & make a PR for it    

# metadata in 
# https://github.com/yt-dlp/yt-dlp#modifying-metadata

from glob import iglob
from pprint import pprint
import subprocess, argparse
from mutagen._file import File, FileType as AudioFile
from mutagen._util import MutagenError
import os

__version__ = 0.4
attributes = ( 
            'album', 
            'albumartist', 
            'artist',
            'copyright', 
            'date',
            'discnumber', 
            'encodedby', 
            'genre', 
            'title', 
            'tracknumber'
)

def get_args() -> argparse.Namespace:
    # NOTE: don't get any funny ideas to map through a list to get these
    # NOTE: date excluded on purpose
    parser = argparse.ArgumentParser(prog='yt-music',
        description="Downloads YouTube videos as music with overwritable metadata.")
    parser.add_argument('links', nargs="*",default="", type=str,
                        help='Space-separated links to download')
    parser.add_argument('-v', '--version', action='version',
                        version=f"%(prog)s {__version__}")
    parser.add_argument('-p', '--path', default="temp") 
    parser.add_argument('-a', '--artist', action='append', metavar='ARTIST(S)')
    parser.add_argument('-A', '--album')
    parser.add_argument('--albumartist') # --Aa misbehaved in help
    parser.add_argument('-c', '--copyright')
    parser.add_argument('-d', '--description')
    parser.add_argument('-D', '--discnumber')
    parser.add_argument('-e', '--encodedby')
    parser.add_argument('-g', '--genre',)
    parser.add_argument('-t', '--title')
    parser.add_argument('-T', '--tracknumber')
    return parser.parse_args()

def parse_tag(tag:str, args:argparse.Namespace, file:AudioFile) -> list[str]|None:
    if (a_tag := vars(args).get(tag)) is not None:
        if type(a_tag) != list:
            return [a_tag]
        return a_tag
    
    if (f_tag := file.get(tag)) is not None:
        if tag == 'date':   # YYYY-MM-DD format
            try:
                temp = str(int(f_tag[0]))      # type:ignore
                return [f'{temp[:4]}-{temp[4:6]}-{temp[6:]}']
            except (ValueError, TypeError): 
                pass
        return f_tag

    return None
    
def save_meta(args:argparse.Namespace, file:AudioFile): 
    # parse tags and strip of empty values
    d = { tag : parsed
        for tag in attributes
        if (parsed := parse_tag(tag, args, file)) is not None
    }

    file.update(d)
    
    try:
        file.save()
    except MutagenError:
        raise ValueError("File couldn't be saved")
    
def download_urls(args:argparse.Namespace) -> list[str]:
    if 0 != subprocess.call((
            'yt-dlp',
            '-x', '-q', '--progress',
            '--embed-metadata',
            '--embed-thumbnail',
            '-o', f'{args.path}/%(title)s.%(ext)s',
            " ".join(args.links)),
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.STDOUT
    ):
        pass
    

if __name__ == "__main__":
    args =  get_args()
    # print(*download_urls(args),sep='\n')

    path:str = p if (p:=args.path) else '.'
    print(*os.walk(path))










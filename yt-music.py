#!/usr/bin/python3

# NOTE: possibly use https://pypi.org/project/rich-argparse/
# TODO: turn every audio file's artist tag into a proper array & make a PR for it    

# metadata in 
# https://github.com/yt-dlp/yt-dlp#modifying-metadata

from glob import iglob
from pprint import pprint
import subprocess, argparse
from mutagen._file import File, FileType as AudioFile

__version__ = 0.2
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
            'tracknumber', 
)
# TODO: redo all of this shit...

def get_args() -> argparse.Namespace:
    # NOTE: don't get any funny ideas to map through a list to get these
    # NOTE: date excluded on purpose
    parser = argparse.ArgumentParser(prog='yt-music',
        description="Downloads YouTube videos as music with overwritable metadata.")
    parser.add_argument('links', nargs="+",
                        help='Space-separated links to download')
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
    parser.add_argument('-v', '--version', action='version',
                    version=f"%(prog)s {__version__}")
    return parser.parse_args()

def parse_tag(tag:str, args:argparse.Namespace, file:AudioFile) -> list[str]|None:
    if (a_tag := vars(args).get(tag)) is not None:
        return a_tag
    
    if (f_tag := file.get(tag)) is not None:
        if tag == 'date':   # YYYY-MM-DD format
            try:
                temp = str(int(f_tag[0]))      # type:ignore
                return [f'{temp[:4]}-{temp[4:6]}-{temp[6:]}']
            except (ValueError, TypeError): 
                pass
        return f_tag

    return []
    



def save_meta(args:argparse.Namespace, file:AudioFile) -> dict: 
    return {}

if __name__ == "__main__":
    args =  get_args()

    for f in iglob("./samples/*"):
        file:AudioFile = File(f, easy=True)    # type:ignore

        print(f)
        print("-"*len(f))
        for i in attributes:
            print(i + '\t\t' + str(parse_tag(i, args, file)))
        
        # a_keys = set(vars(args).keys())
        # f_keys = set(file.keys())
        #
        # # pprint(save_meta(args, File(f, easy=True)))
        # pprint(a_keys.intersection(f_keys))
        print()
        



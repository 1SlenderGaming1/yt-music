#!/usr/bin/python3

# NOTE: possibly use https://pypi.org/project/rich-argparse/

import subprocess, argparse
from mutagen._file import File, FileType as AudioFile

__version__ = 0.1
attributes = ( 'album', 'copyright', 'encodedby', 'title', 'artist', 'albumartist', 'discnumber', 'tracknumber', 'genre', 'date' )
# TODO: redo all of this shit...

def get_args() -> argparse.Namespace:
    # don't get any funny ideas to map through a list to get these
    parser = argparse.ArgumentParser(prog='yt-music',
        description="Downloads YouTube videos as music with overwritable metadata.")
    parser.add_argument('links', nargs="+",
                        help='Space-separated links to download')
    parser.add_argument('-a', '--artist', action='append', metavar='ARTIST(S)')
    parser.add_argument('-A', '--album')
    parser.add_argument('--albumartist') # --Aa misbehaved in help
    parser.add_argument('-c', '--copyright')
    parser.add_argument('-d', '--description')
    parser.add_argument('-D', '--discnumber', type=int)
    parser.add_argument('-e', '--encodedby')
    parser.add_argument('-g', '--genre',)
    parser.add_argument('-t', '--title', dest='title')
    parser.add_argument('-T', '--tracknumber', dest='tracknumber')
    parser.add_argument('-v', '--version', action='version',
                    version=f"%(prog)s {__version__}")
    return parser.parse_args()

def parse_artists(artists: list[str]):
    artists.sort()
    return ' / '.join(artists)

def parse_to_dict(f:AudioFile) -> dict: 
    return {}


if __name__ == "__main__":
    f:AudioFile = File('./samples/sample.mp3', easy=True) # type:ignore
    f.update({ 'artist':'TEST_ARTIST/TEST_ARTIST2' })
    f.save()

    # print(f.tags['artist'])

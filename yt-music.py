#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from collections.abc import Generator
from glob import iglob
from pprint import pprint

from mutagen._util import MutagenError
from mutagen.oggopus import Open as OggOpen
from pytube import Playlist, YouTube
from pytube.exceptions import RegexMatchError
import yt_dlp

__version__ = 0.7

type Options = dict

current_filename = ""


def main():
    args =  get_args()
    OPTS = {
        "quiet": args.quiet,
        'overwrites':True,
        'outtmpl':{ 'default':f'{args.path}%(title)s.opus' },
        'format':'bestaudio/best',
        'postprocessors':[
            { 'key':'FFmpegExtractAudio', 'preferredcodec':'opus' },
            { 'key':'EmbedThumbnail' },
        ]
    }
    
    # https://www.youtube.com/watch?v=tu4OQ8LQn4w&list=OLAK5uy_kmYYWT5HDnLkg0Jo_CepBLnZc7DuR5OiM


    for filepath, link, playlist in download_audio(OPTS, args):
        parse_metadata(link, args, playlist)




def get_args() -> Namespace:
    parser = ArgumentParser(prog='yt-music',
        description="Downloads YouTube videos as music with overwritable metadata.")
    parser.add_argument('links', nargs="*",default="", type=str,
                        help='Space-separated links to download')
    parser.add_argument('-v', '--version', action='version',
                        version=f"%(prog)s {__version__}")
    parser.add_argument('-q', '--quiet', action="store_true")
    parser.add_argument('-p', '--path', default="./", type=dir_path) 

    parser.add_argument('-A', '--album')
    parser.add_argument('-l', '--albumartist')
    parser.add_argument('-a', '--artist', action='append', metavar='ARTIST(S)')
    parser.add_argument('-g', '--genre')
    parser.add_argument('-t', '--title')
    return parser.parse_args()

def save_meta(filepath:str, metadata:dict, args):
    file = OggOpen(filepath)
    link=''
    # parse_metadata(link, args, )
    
    # if file is None:
    #     raise ValueError(f"{filepath} was not found.")

    # file

    pass

def parse_metadata(link:str, args:Namespace, 
                   playlist: Playlist|None = None,
                   index:int|None = None) -> dict[str,str]:
    """Parse and merge metadata from arguments and video link into a single dict.

    - link: video link
    - args: user arguments
    - playlist: playlist object
    - index: current position of playlist, pass via enumerate()
    """

    vid = YouTube(link)

    if playlist is None and 'list=' in link:
        playlist = Playlist("https://youtube.com/playlist?list="+link.split("list=")[1])
    
    d = {
        'artist':vid.author,
        'albumartist': vid.author,
        'comment': f"{vid.watch_url}{_des+'\n' if ( _des:=vid.description) else ''}",
        'date': vid.publish_date.strftime('%Y-%m-%d'), # type:ignore
        'title': vid.title,
    }

    if playlist is not None:
        d['tracknumber'] = f"{index}/{playlist.length}"
        d['albumartist'] = vid.author,
        d['album'] = playlist.title

    overwrite = { k:v for k,v in {
        'album': args.album,
        'albumartist': args.albumartist,
        'artist': args.artist,
        'genre': args.genre,
        'title': args.title,
        }.items() if v is not None }

    return {**d, **overwrite}

def download_audio(opts: dict, args:Namespace) -> Generator[tuple[str, str, Playlist|None], None, None]:
    """
    Downloads videos and applies thumbnails.
    Returns expected filepaths.
    """

    links:list[str] = args.links   

    with yt_dlp.YoutubeDL(opts) as yt:
        for link in links:
            if "playlist?list=" in link:
                try:
                    links.extend(Playlist(link))
                    print("Appending playlist to download queue")
                    continue
                except RegexMatchError:
                    print("Skipping ", link)
                    continue

            # validate and strip link
            try:
                l = YouTube(link).watch_url
            except RegexMatchError:
                print('Skipping ', link)
                continue

            info:dict    = yt.extract_info(l, download=True) # type:ignore
            filename:str = info['entries'][0]['requested_downloads'][0]['filename']

            try:
                playlist = Playlist(link)
            except RegexMatchError:
                playlist=None

            yield filename, l, playlist
    return None

def dir_path(p:str) -> str:
    return p if p.endswith("/") else p + "/"

if __name__ == "__main__":
    main()

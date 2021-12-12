#!/usr/bin/env python
from __future__ import unicode_literals

import json
import os
import re
import sys

import eyed3
import yt_dlp
from eyed3.core import Date


def simplify_string(string: str) -> str:
    """Remove special symbols end extra spaces.

    :param string: what is needed to simplify
    :return: simplified string
    """
    simpl1 = re.sub(r'[^\w\d\-. ]', '', string)
    simpl2 = re.sub(r'[ ]+', ' ', simpl1)
    return simpl2


def set_id3_tag(file: str, info: dict, title: str) -> None:
    upl = simplify_string(info.get('uploader', '-'))
    audiofile = eyed3.load(file)
    audiofile.tag.recording_date = Date(int(info['upload_date'][:4]),
                                        month=int(info['upload_date'][4:6]),
                                        day=int(info['upload_date'][6:]))
    audiofile.tag.title = title
    audiofile.tag.artist = upl
    audiofile.tag.album = simplify_string(info.get('uploader', file[:-4]))
    audiofile.tag.album_artist = upl if not info.get(
        'tags', '') else info.get('tags', ['-'])[0]
    audiofile.tag.save()


def complete_hook(d):
    if d['status'] == 'finished':
        print('[info] Downloading completed, now converting ...')


def get_options(hook) -> dict:
    return {
        'useragent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
        'referer': 'https://www.youtube.com/',
        'writethumbnail': True,
        'format': 'bestaudio/best',
        'writeinfojson': True,
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [hook],
        'download_archive': './.yt_archive.txt',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3',
             'preferredquality': '192'},
            {'key': 'EmbedThumbnail'}]
    }


def download_task_list(task_list: str) -> None:
    """Main function where task_list processed by youtube_dl

    :param task_list: path to text file with links"""
    with open(task_list) as fd:
        for url in fd:
            with yt_dlp.YoutubeDL(get_options(complete_hook)) as ydl:
                try:
                    ydl.download([url])
                except yt_dlp.DownloadError as e:
                    print(f'[error] Download failed. {e}')


def process_downloaded_mp3() -> None:
    """Function sets mp3 tags, renames files and removes temporary files."""
    for file in os.listdir(os.curdir):
        if file.lower().endswith('.mp3'):
            file_name = file[:-4]
            info_json = file_name + '.info.json'
            if os.path.exists(info_json):
                with open(info_json) as jf:
                    info = json.load(jf)
                title = simplify_string(info.get('title', '-'))
                print('[info] Setting id3 tags to', title)
                set_id3_tag(file, info, title)
                simpl_name = simplify_string(
                    (title.replace(' - ', '_') + '.mp3').replace('..', '.'))
                os.rename(file, simpl_name)
                os.remove(info_json)


if __name__ == '__main__':
    download_task_list(sys.argv[1])
    process_downloaded_mp3()

    input('\nPress enter to exit...')

#!/usr/bin/env python
from __future__ import unicode_literals

import eyed3
import json
import os
import re
import youtube_dl
from eyed3.core import Date


def simplify_string(string: str) -> str:
    """Remove special symbols end extra spaces.

    :param string: what is needed to simplify
    :return: simplified string
    """
    simpl1 = re.sub(r'[/,~&№^:;+%@!?#*{}|<>`\"\'\[\]\\]', '', string)
    simpl2 = re.sub(r'[ ]+', ' ', simpl1)
    return simpl2


def set_id3_tag(file: str, info: dict, title: str):
    upl = simplify_string(info.get('uploader', '-'))
    audiofile = eyed3.load(file)
    audiofile.tag.recording_date = Date(int(info['upload_date'][:4]),
                                        month=int(info['upload_date'][4:6]),
                                        day=int(info['upload_date'][6:]))
    audiofile.tag.title = title
    audiofile.tag.artist = upl
    audiofile.tag.album = simplify_string(info.get('uploader', file_name))
    audiofile.tag.album_artist = upl if not info.get('tags', '') else info.get('tags', ['-'])[0]
    audiofile.tag.save()


def my_hook(d):
    if d['status'] == 'finished':
        print('[info] Downloading completed, now converting ...')


ydl_opts = {
    'writethumbnail': True,
    'format': 'bestaudio/best',
    'writeinfojson': True,
    'outtmpl': '%(title)s.%(ext)s',
    'progress_hooks': [my_hook],
    'download_archive': './.yt_archive.txt',
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
         'preferredcodec': 'mp3',
         'preferredquality': '192'},
        {'key': 'EmbedThumbnail'}]
}

with open('tasklist.txt') as f:
    urls = f.readlines()

failed_urls = []

for url in urls:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except youtube_dl.DownloadError as e:
            print(f'[error] Download failed. {e}')
            failed_urls.append(url)

with open('failed_tasks.txt', 'w') as f:
    f.writelines(failed_urls)

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
            simpl_name = simplify_string((title.replace(' - ', '_') + '.mp3').replace('..', '.'))
            os.rename(file, simpl_name)
            os.remove(info_json)

if len(failed_urls) != 0:
    print('\n[warning] There was failed tasks. See url in {failed_tasks.txt}.')

input('\nPress enter to exit...')

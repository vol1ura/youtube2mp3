from __future__ import unicode_literals
import youtube_dl
from eyed3.core import Date
import eyed3
import json
import os
import re


def simplify_string(string: str) -> str:
    """Remove special symbols end extra spaces.

    :param string: what is needed to simplify
    :return: simplified string
    """
    simpl1 = re.sub(r'[/,~&№^:;+%@!?#*{}|()<>`\"\'\[\]\\]', '', string)
    simpl2 = re.sub(r'[ ]+', ' ', simpl1)
    return simpl2


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'writethumbnail': True,
    'format': 'bestaudio/best',
    'writeinfojson': True,
    'outtmpl': '%(title)s.%(ext)s',
    'progress_hooks': [my_hook],
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
         'preferredcodec': 'mp3',
         'preferredquality': '192'},
        {'key': 'EmbedThumbnail'}]
}

with open('tasklist.txt') as f:
    urls = f.readlines()

for url in urls:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

for file in os.listdir('./'):
    if file.lower().endswith('.mp3'):
        file_name = file[:-4]
        info_json = file_name + '.info.json'
        if os.path.exists(info_json):
            with open(info_json) as jf:
                info = json.load(jf)
            thumbnail = info.get('thumbnail', '')
            upl = simplify_string(info.get('uploader', '-'))
            title = simplify_string(info.get('title', '-'))
            print('Setting id3 tags to ', title)
            audiofile = eyed3.load(file)
            audiofile.tag.recording_date = Date(int(info['upload_date'][:4]),
                                                month=int(info['upload_date'][4:6]),
                                                day=int(info['upload_date'][6:]))
            audiofile.tag.title = title
            audiofile.tag.artist = upl
            audiofile.tag.album = simplify_string(info.get('uploader', file_name))
            audiofile.tag.album_artist = upl if not info.get('tags', '') else info.get('tags', ['-'])[0]
            audiofile.tag.save()
            simpl_name = simplify_string((title.replace(' - ', '_') + '.mp3').replace('..', '.'))
            os.rename(file, simpl_name)
            os.remove(info_json)

input('Press enter to exit...')

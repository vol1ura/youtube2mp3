[![Quality&Tests](https://github.com/vol1ura/youtube2mp3/actions/workflows/python-app.yml/badge.svg)](https://github.com/vol1ura/youtube2mp3/actions/workflows/python-app.yml)
[![Code Style](https://img.shields.io/badge/Code%20Style-PEP%208-blueviolet)](https://www.python.org/dev/peps/pep-0008/)
[![codecov](https://codecov.io/gh/vol1ura/youtube2mp3/branch/master/graph/badge.svg)](https://codecov.io/gh/vol1ura/youtube2mp3)
![GitHub](https://img.shields.io/github/license/vol1ura/youtube2mp3)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)

# YouTube to mp3 download and convert
Simple Python script to download youtube videos and playlists to mp3 format.
Script based on `yt-dlp` [module](https://github.com/yt-dlp/yt-dlp), and also uses `eyed3` module to add id3 tags.

## Features
* Simplified names of mp3 files
* Special symbols is removed
* Embedded thumbnails
* Added id3 tags with authors and descriptions

## Using
* You need install [ffmpeg](https://www.ffmpeg.org/) to script be able to convert files into mp3.
* Add links to `tasklist.txt`. It can be both videos and playlists.
* Run script `youtube2mp3.py tasklist.txt`.

## In Windows
You can use `exe` file in `dist` folder - no need to install Python interpreter.

![Executable](pics/pic1.png)

## Result in audiopleer

![Executable](pics/pic2.png)

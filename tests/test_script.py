import json
import os

import eyed3
import pytest as pytest
import youtube_dl

import youtube2mp3


@pytest.mark.parametrize('string, expected', (('test!@#$%^&*()-+1', 'test-1'), ('1   ,.', '1 .')))
def test_simplify_string(string, expected):
    assert youtube2mp3.simplify_string(string) == expected


@pytest.mark.parametrize('d, result', (({'status': 'finished'}, True), ({'status': 'in process'}, False)))
def test_complete_hook(d, result, capsys):
    youtube2mp3.complete_hook(d)
    out, _ = capsys.readouterr()
    assert ('[info]' in out) is result


def test_get_options():
    result = youtube2mp3.get_options('hook')
    keys = ('writethumbnail', 'format', 'writeinfojson', 'outtmpl',
            'progress_hooks', 'download_archive', 'postprocessors')
    assert all(key in result for key in keys)


def test_process_downloaded_mp3(tmpdir, monkeypatch):
    # prepare test environment
    working_dir = tmpdir.mkdir('working_dir')
    working_dir.join('test_1.mp3').write('test')
    working_dir.join('test_2.mp3').write('test with no json info file')
    json_file = working_dir.join('test_1.info.json')
    json_file.write(json.dumps({'title': 'test - title.'}))
    monkeypatch.setattr(youtube2mp3, 'set_id3_tag', lambda *args: None)
    os.chdir(working_dir)
    # run tested function
    youtube2mp3.process_downloaded_mp3()
    # checking assertions
    assert not os.path.exists(json_file.basename)
    assert os.path.exists('test_title.mp3')


def test_set_id3_tag(tmpdir):
    tmp_file = tmpdir.join('downloaded_track.mp3')
    for_test = os.path.join(os.path.dirname(__file__), 'for_test.mp3')
    with open(for_test, 'rb') as fd_r, open(tmp_file, 'wb') as fd_w:
        fd_w.write(fd_r.read())
    info = {
        'uploader': 'Andrew Codeman',
        'upload_date': '20180101',
        'title': 'Bear with a guitar',
        'tags': ['CC BY 4.0']
    }
    youtube2mp3.set_id3_tag(str(tmp_file), info)
    audiofile = eyed3.load(tmp_file)
    assert audiofile.tag.recording_date.year == 2018
    assert audiofile.tag.title == info['title']
    assert audiofile.tag.artist == info['uploader']
    assert audiofile.tag.album == info['uploader']
    assert audiofile.tag.album_artist == info['tags'][0]


def test_download_task_list(monkeypatch, tmpdir, capsys):
    task_list = tmpdir.join('task_list.txt')
    task_list.write('test')

    def mock_download_error(*args):
        raise youtube_dl.DownloadError('test download error')

    monkeypatch.setattr(youtube_dl.YoutubeDL, 'download', mock_download_error)
    youtube2mp3.download_task_list(task_list)
    out, err = capsys.readouterr()
    assert '[error]' in out
    assert err == ''

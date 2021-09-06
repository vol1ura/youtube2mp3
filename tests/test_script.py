import json
import os

import pytest as pytest

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
    working_dir.join('test.mp3').write('test')
    json_file = working_dir.join('test.info.json')
    json_file.write(json.dumps({'title': 'test - title.'}))
    monkeypatch.setattr(youtube2mp3, 'set_id3_tag', lambda *args: None)
    os.chdir(working_dir)
    # run tested function
    youtube2mp3.process_downloaded_mp3()
    # checking assertions
    assert not os.path.exists(json_file.basename)
    assert os.path.exists('test_title.mp3')


def test_set_id3_tag():
    pass


def test_download_task_list():
    pass

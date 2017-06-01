from __future__ import unicode_literals

import sys
import youtube_dl
import urlparse

AUDIO_DATA_FOLDER = 'data/audio/'
VIDEO_DATA_FOLDER = 'data/video/'


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def audio_hook(d):
    if d['status'] == 'finished':
        print('Done downloading audio, now converting ...')


def video_hook(d):
    if d['status'] == 'finished':
        print('Done downloading video')


def get_youtube_id(url):
    url_data = urlparse.urlparse(url)
    query = urlparse.parse_qs(url_data.query)
    return query["v"][0]


def download_audio(url, options=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav'
        }],
        'logger': MyLogger(),
        'progress_hooks': [audio_hook],
        'outtmpl': '{}%(id)s.%(ext)s'.format(AUDIO_DATA_FOLDER),
        'restrictfilenames': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    youtube_id = get_youtube_id(url)
    return AUDIO_DATA_FOLDER + youtube_id + '.wav'


def download_video(url, options=None):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best',
        'logger': MyLogger(),
        'progress_hooks': [video_hook],
        'outtmpl': '{}%(id)s.%(ext)s'.format(VIDEO_DATA_FOLDER),
        'restrictfilenames': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    youtube_id = get_youtube_id(url)
    return VIDEO_DATA_FOLDER + youtube_id + '.mp4'

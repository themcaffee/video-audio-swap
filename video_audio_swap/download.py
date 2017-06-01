from __future__ import unicode_literals

import sys
import youtube_dl
from urllib.parse import urlparse, parse_qs

AUDIO_DATA_FOLDER = 'data/audio/'
VIDEO_DATA_FOLDER = 'data/video/'


class MyLogger(object):
    """
    Logger that keeps track of youtube-dl statuses
    """
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def audio_hook(d):
    """
    Executed when events happen from downloading youtube audio
    :param d:
    :return:
    """
    if d['status'] == 'finished':
        print('Done downloading audio, now converting ...')


def video_hook(d):
    """
    Executed when events happen from downloading a youtube video
    :param d:
    :return:
    """
    if d['status'] == 'finished':
        print('Done downloading video')


def get_youtube_id(url):
    """
    Parse the youtube id from the given youtube url
    :param url:
    :return:
    """
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    return query["v"][0]


def download_audio(url, options=None):
    """
    Download the audio track of the given youtube url
    :param url: A full youtube url
    :param options:
    :return:
    """
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

    # Parse and return the output file
    youtube_id = get_youtube_id(url)
    return AUDIO_DATA_FOLDER + youtube_id + '.wav'


def download_video(url, options=None):
    """
    Download the video of the given youtube url
    :param url: A full youtube url
    :param options:
    :return:
    """
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4/best',
        'logger': MyLogger(),
        'progress_hooks': [video_hook],
        'outtmpl': '{}%(id)s.%(ext)s'.format(VIDEO_DATA_FOLDER),
        'restrictfilenames': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Parse and return the output file
    youtube_id = get_youtube_id(url)
    return VIDEO_DATA_FOLDER + youtube_id + '.mp4'

#! /usr/bin/env python

import argparse

from video_audio_swap.download import download_audio
from video_audio_swap.download import download_video
from video_audio_swap.swap import get_file_bpm, get_tempo

parser = argparse.ArgumentParser(description='Swap the video and audio of a music video and music track')
parser.add_argument('--audio-youtube', dest='audio_youtube',
                    help='The youtube audio url')
parser.add_argument('--video-youtube', dest='video_youtube',
                    help='The youtube video url')
parser.add_argument('--audio-file', dest='audio_file',
                    help='The location of the audio file')
parser.add_argument('--video-file', dest='video_file',
                    help='The location of the video file')
"""
# super fast
samplerate, win_s, hop_s = 4000, 128, 64
# fast
samplerate, win_s, hop_s = 8000, 512, 128
# default:
# samplerate, win_s, hop_s = 44100, 1024, 512
"""
parser.add_argument('--samplerate', dest='samplerate', type=int, default=48000,
                    help='The sample rate of the audio track')
parser.add_argument('--win_s', dest='win_s', type=int, default=512)
parser.add_argument('--hop_s', dest='hop_s', type=int, default=128)

args = parser.parse_args()

# Example
# https://www.youtube.com/watch?v=Oa-ae6_okmg

# Download the audio and video from youtube
if 'audio_youtube' in args:
    audio_file = download_audio(args.audio_youtube)
else:
    audio_file = args.audio_file

if 'video_youtube' in args:
    video_file = download_video(args.video_youtube)
else:
    video_file = args.video_file

# Get information about the audio track
get_file_bpm(audio_file, args.samplerate, args.win_s, args.hop_s)
get_tempo(audio_file, args.samplerate, args.win_s, args.hop_s)

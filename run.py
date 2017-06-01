#! /usr/bin/env python

import argparse
from pprint import pprint

from video_audio_swap.download import download_audio, clear_audio_folder, clear_video_folder
from video_audio_swap.download import download_video
from video_audio_swap.swap import get_file_bpm, get_tempo, save_audio_from_video, combine_video_audio, get_track_length, \
    set_video_rate

parser = argparse.ArgumentParser(description='Swap the video and audio of a music video and music track')
parser.add_argument('--audio-youtube', dest='audio_youtube',
                    help='The youtube audio url')
parser.add_argument('--video-youtube', dest='video_youtube',
                    help='The youtube video url')
parser.add_argument('--audio-file', dest='audio_file',
                    help='The location of the audio file')
parser.add_argument('--video-file', dest='video_file',
                    help='The location of the video file')
parser.add_argument('--clear', dest='clear', action='store_true',
                    help='Delete all stored temp files from audio and video folders')
parser.set_defaults(clear=False)
parser.add_argument('--output', dest='output', default='final_output',
                    help='The path and name of the output file')


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

parser.add_argument('--video-samplerate', dest='video_samplerate', type=int, default=48000,
                    help="The sample rate of the video track's audio")
parser.add_argument('--video-win_s', dest='video_win_s', type=int, default=512)
parser.add_argument('--video-hop_s', dest='video_hop_s', type=int, default=128)

args = parser.parse_args()

# Clear audio and video folder files if enabled
if args.clear:
    clear_audio_folder()
    clear_video_folder()

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
audio_bpm = get_file_bpm(audio_file, args.samplerate, args.win_s, args.hop_s)
audio_length = get_track_length(audio_file)
print(str(audio_length))

# Seperate the audio file out of the video file to find bpm
video_split_audio = save_audio_from_video(video_file)

print(video_split_audio)
video_bpm = get_file_bpm(video_split_audio, args.video_samplerate, args.video_win_s, args.video_hop_s)
video_length = get_track_length(video_split_audio)
print(str(video_length))

bpm_ratio = audio_bpm / video_bpm
print(bpm_ratio)

set_video_rate(video_file, rate=bpm_ratio)

combined_path = combine_video_audio(video_file, audio_file, args.output)
print("Finished! See result at: " + combined_path)

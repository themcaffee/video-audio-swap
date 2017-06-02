#! /usr/bin/env python

import argparse
import datetime

from video_audio_swap.download import download_audio, clear_data_folders
from video_audio_swap.download import download_video
from video_audio_swap.helpers import parse_timedelta
from video_audio_swap.swap import get_file_bpm, save_audio_from_video, combine_video_audio, get_track_length, \
    set_video_rate, cut_video

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


parser.add_argument('--video-start', dest='video_start',
                    help="Where the music video's audio track starts playing")
parser.add_argument('--video-end', dest='video_end',
                    help="Where the music video's audio track ends")
parser.add_argument('--audio-start', dest='audio_start',
                    help="Where the audio in the given audio track starts")
parser.add_argument('--audio-end', dest='audio_end',
                    help="Where the audio in the given audio track stops")


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
    clear_data_folders()

# Download the audio and video from youtube
if args.audio_youtube:
    audio_file = download_audio(args.audio_youtube)
else:
    audio_file = args.audio_file
if args.video_youtube:
    video_file = download_video(args.video_youtube)
else:
    video_file = args.video_file

# Parse the times of start / end
if args.audio_start:
    audio_start = parse_timedelta(args.audio_start)
if args.audio_end:
    audio_end = parse_timedelta(args.audio_end)

# Get information about the audio track
audio_bpm = get_file_bpm(audio_file, args.samplerate, args.win_s, args.hop_s)
print("Audio track bpm: " + str(audio_bpm))

# Get the length of the video track
if args.audio_start and args.audio_end:
    audio_length = args.audio_end - args.audio_start
elif args.audio_end:
    audio_length = args.audio_end
elif args.video_start:
    audio_length = get_track_length(audio_file) - args.audio_start
else:
    audio_length = get_track_length(audio_file)
print("Audio track length: " + str(audio_length))

# Get the start and end of the video (user or file defined)
original_video_length = get_track_length(video_file)
if args.video_start:
    video_start = parse_timedelta(args.video_start)
else:
    video_start = datetime.timedelta(seconds=0)
if args.video_end:
    video_end = parse_timedelta(args.video_end)
else:
    video_end = original_video_length
video_length = video_end - video_start
print("Video track length: " + str(video_length))

# Cut the video if necessary
if video_length != original_video_length:
    print("Cutting video...")
    video_file = cut_video(video_file, video_start, video_end)

# Seperate the audio file out of the video file to find bpm
video_split_audio = save_audio_from_video(video_file)
video_bpm = get_file_bpm(video_split_audio, args.video_samplerate, args.video_win_s, args.video_hop_s)
print('Video audio track bpm: ' + str(video_bpm))

# Determine how much to adjust track to match bpm
bpm_ratio = audio_bpm / video_bpm
print("audio:video bpm ratio: " + str(bpm_ratio))

# Speed up / slow down video to match bpm
print("Adjusting video to " + str(bpm_ratio) + " the speed. This may take awhile..")
adjusted_video = set_video_rate(video_file, rate=bpm_ratio)

# Combine the adjusted video and new audio track
combined_path = combine_video_audio(adjusted_video, audio_file, args.output)
print("Finished! See result at: " + combined_path)

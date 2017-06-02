import re
import subprocess

import datetime

from aubio import source, tempo
from numpy import median, diff

from video_audio_swap.config import ADJUSTED_AUDIO_FOLDER, ADJUSTED_VIDEO_FOLDER, VIDEO_DATA_FOLDER, BEATS_DATA_FOLDER


FFMPEG_LOG_LEVEL = 'warning'


def get_file_bpm(path, samplerate, win_s, hop_s):
    """
    Get the bpm of the given audio track
    :param path: The path to the audio track
    :param samplerate:
    :param win_s:
    :param hop_s:
    :return:
    """
    s = source(path, samplerate, hop_s)
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    # Convert to periods and to bpm
    if len(beats) > 1:
        if len(beats) < 4:
            raise Exception("few beats found")
        bpms = 60./diff(beats)
        b = median(bpms)
    else:
        b = 0
        raise Exception("Not enough beats found")

    return b


def get_tempo(path, samplerate, win_s, hop_s):
    """
    Get the current tempo of the given track and write it
    to a file
    :param path: Path to the audio track
    :param samplerate:
    :param win_s:
    :param hop_s:
    :return:
    """
    s = source(path, samplerate, hop_s)
    o = tempo("default", win_s, hop_s, samplerate)

    # tempo detection delay, in samples
    # default to 4 blocks delay to catch up with
    delay = 4. * hop_s

    # list of beats, in samples
    beats = []

    # total number of frames read
    total_frames = 0
    log_filename = path.rsplit('/', 1)[-1]
    log_file = open(BEATS_DATA_FOLDER + log_filename + '.txt', 'w')
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            beat_info = "%f" % (this_beat / float(samplerate))
            log_file.write(beat_info)
            log_file.write("\n")
            # print(beat_info)
            beats.append(this_beat)
        total_frames += read
        if read < hop_s: break
    return beats


def set_video_rate(path, rate=0.5):
    """
    Set the video speed using ffmpeg
    :param path: The path to the video
    :param rate: The rate to speed up / slow down the video
    :return:
    """
    out_path = ADJUSTED_VIDEO_FOLDER + 'output.mp4'
    cmd = 'ffmpeg -loglevel {} -y -i {} -strict -2 -filter:v setpts={}*PTS {}'.format(FFMPEG_LOG_LEVEL, path, str(rate), out_path).split(" ")
    subprocess.run(cmd)
    return out_path


def set_audio_rate(path, rate=2.0):
    """
    Set the audio tempo of a track using ffmpeg.
    NOTE: Currently only supports rates from 0.5 to 2.0. See https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video
    :param path: The path to the audio file
    :param rate: The rate to speed up / slow down the track
    :return:
    """
    out_path = ADJUSTED_AUDIO_FOLDER + 'output.wav'
    cmd = 'ffmpeg  -loglevel {} -y -i {} -filter:a "atempo={} -vn {}'.format(FFMPEG_LOG_LEVEL, path, str(rate), out_path).split(" ")
    subprocess.run(cmd)
    return out_path


def get_track_length(path):
    """
    Get an audio track length using ffmpeg
    :param path:
    :return:
    """
    process = subprocess.Popen(['ffmpeg',  '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),".encode('utf-8'), stdout, re.DOTALL).groupdict()
    matches['hours'] = int(matches['hours'].decode('utf-8'))
    matches['minutes'] = int(matches['minutes'].decode('utf-8'))
    matches['seconds'] = int(matches['seconds'].decode('utf-8').split(".")[0])
    return datetime.timedelta(hours=matches['hours'], minutes=matches['minutes'], seconds=matches['seconds'])


def combine_video_audio(video_path, audio_path, output_path):
    """
    Replace the audio track of the video file with the given audio path
    :param video_path: Path to the video file
    :param audio_path: Path to the audio file
    :return:
    """
    output_path += ".mp4"
    cmd = 'ffmpeg -loglevel {} -y -i {} -i {} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 {}'.format(FFMPEG_LOG_LEVEL, video_path, audio_path, output_path).split(" ")
    subprocess.run(cmd)
    return output_path


def save_audio_from_video(video_path):
    """
    Save the audio of a mp4 to wav
    :param video_path: The path to the video file
    :return:
    """
    out_path = VIDEO_DATA_FOLDER + 'output.wav'
    cmd = 'ffmpeg -loglevel {} -y -i {} -acodec pcm_s16le -ac 2 {}'.format(FFMPEG_LOG_LEVEL, video_path, out_path).split(" ")
    subprocess.run(cmd)
    return out_path


def cut_video(video_path, start, stop):
    out_path = VIDEO_DATA_FOLDER + 'cut.mp4'
    cmd = 'ffmpeg -loglevel {} -y -ss {} -i {} -to {} -c copy {}'.format(FFMPEG_LOG_LEVEL, start, video_path, stop, out_path).split(" ")
    subprocess.run(cmd)
    return out_path

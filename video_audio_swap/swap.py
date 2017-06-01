from aubio import source, tempo
from numpy import median, diff


# Path to the folder that holds the tempo time info
BEATS_DATA_FOLDER = 'data/beats/'


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
            print("few beats found")
        bpms = 60./diff(beats)
        b = median(bpms)
    else:
        b = 0
        print("not enough beats found")

    print("{:6s} {:s}".format("{:2f}".format(b), path))
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
    print(len(beats))


def set_video_rate(path, rate=0.5):
    """
    Set the video speed using ffmpeg
    :param path: The path to the video
    :param rate: The rate to speed up / slow down the video
    :return:
    """
    out_path = 'output.mp4'
    cmd = 'ffmpeg -i {} -filter:v "setpts={}*PTS" -strict -2 {}'.format(path, str(rate), out_path)


def set_audio_rate(path, rate=2.0):
    """
    Set the audio tempo of a track using ffmpeg.
    NOTE: Currently only supports rates from 0.5 to 2.0. See https://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video
    :param path: The path to the audio file
    :param rate: The rate to speed up / slow down the track
    :return:
    """
    out_path = 'output.wav'
    cmd = 'ffmpeg -i {} -filter:a "atempo={} -vn {}'.format(path, str(rate), out_path)


def combine_video_audio(video_path, audio_path):
    """
    Combine the video and audio tracks
    :param video_path: Path to the video file
    :param audio_path: Path to the audio file
    :return:
    """
    out_path = 'output.mp4'
    cmd = 'ffmpeg -i {} -i {} -c:v copy -c:a -strict experimental {}'.format(video_path, audio_path, out_path)


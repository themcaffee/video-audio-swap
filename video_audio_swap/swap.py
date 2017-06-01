from aubio import source, tempo
from numpy import median, diff


def get_file_bpm(path, samplerate, win_s, hop_s):
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
    s = source(path, samplerate, hop_s)
    o = tempo("default", win_s, hop_s, samplerate)

    # tempo detection delay, in samples
    # default to 4 blocks delay to catch up with
    delay = 4. * hop_s

    # list of beats, in samples
    beats = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            print("%f" % (this_beat / float(samplerate)))
            beats.append(this_beat)
        total_frames += read
        if read < hop_s: break
    print(len(beats))

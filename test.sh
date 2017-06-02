#!/bin/bash

VIDEO="https://www.youtube.com/watch?v=l3wjcwTcfT4"
AUDIO="https://www.youtube.com/watch?v=Oa-ae6_okmg"

./run.py --video-youtube "$VIDEO" --audio-youtube "$AUDIO" --video-samplerate 44100

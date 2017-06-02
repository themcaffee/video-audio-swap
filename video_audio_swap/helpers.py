from pytimeparse import parse
import datetime


def parse_timedelta(input):
    seconds = parse(input)
    return datetime.timedelta(seconds=seconds)

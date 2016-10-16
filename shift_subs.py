#!/usr/bin/env python3

"""
Shift the times in subtitle files.
"""

import sys
import os.path
import argparse
from datetime import datetime, timedelta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add = parser.add_argument  # shortcut
    add('file', metavar='FILE', help='subtitles file')
    add('-o', '--output', metavar='FILE', default='-', help='output file')
    add('--shift', type=int, default=0, help='number of seconds to shift')
    args = parser.parse_args()

    if args.output != '-' and os.path.exists(args.output):
        sys.exit('File exists: %s' % args.output)

    fout = open(args.output, 'wt') if args.output != '-' else sys.stdout
    dt = lambda t: shift_time(t, args.shift)  # shortcut
    for line in open(args.file):
        if ' --> ' in line:  # looks like "02:08:11,080 --> 02:08:14,160"
            t1, t2 = line.split(' --> ')
            fout.write('%s --> %s\n' % (dt(t1), dt(t2)))
        else:
            fout.write(line)


def shift_time(t, dt):
    "Return the time given as 'H:M:S,ms' with a shift of dt seconds"
    h_m_s, ms = t.split(',')
    h, m, s = [int(x) for x in h_m_s.split(':')]
    t0 = datetime(2000, 1, 1, h, m, s, 1000 * int(ms))
    return '{:%H:%M:%S,%f}'.format(t0 + timedelta(seconds=dt))[:-3]



if __name__ == '__main__':
    main()

#! /usr/bin/env python

from __future__ import print_function

import re
import sys


def recover_bed_name(name):
    new_name = re.sub(r'::.+:[0-9]+-[0-9]+\([+-]\)', '', name)
    return new_name


if __name__ == "__main__":
    for line in sys.stdin:
        name, seq = line.rstrip('\n').split('\t')
        new_name = recover_bed_name(name)
        print('\t'.join([new_name, seq]))

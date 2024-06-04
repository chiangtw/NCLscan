#! /usr/bin/env python

from __future__ import print_function

import sys
from itertools import groupby
from operator import itemgetter


def read_file(fileObj):
    for line in fileObj:
        data = line.rstrip('\n').split('\t')
        
        if len(data) != 2:
            continue

        seq_id, seq = data
        yield seq_id, seq


if __name__ == "__main__":
    for seq_id, gp in groupby(read_file(sys.stdin), key=itemgetter(0)):
        merged_seq = ''.join([seq for _, seq in gp])
        print('\t'.join([seq_id, merged_seq]))

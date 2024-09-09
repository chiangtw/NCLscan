#! /usr/bin/env python

from __future__ import print_function

import re
import sys
import argparse


def get_readthrough(result_tmp_file, output_file, readthrough_output_file):
    result_tmp_data = read_TSV(result_tmp_file)

    result_tmp_data_not_readthrough = []
    result_tmp_data_readthrough = []

    for line_list in result_tmp_data:

        chr_d, pos_d, strand_d, chr_a, pos_a, strand_a = line_list[1:7]
        pos_d = int(pos_d)
        pos_a = int(pos_a)

        if (chr_d == chr_a) and (strand_d == strand_a):

            if strand_d == "+":
                if (pos_a > pos_d) and (pos_a - pos_d < 2000000):
                    result_tmp_data_readthrough.append(line_list)
                    continue
            else:
                if (pos_d > pos_a) and (pos_d - pos_a < 2000000):
                    result_tmp_data_readthrough.append(line_list)
                    continue

        result_tmp_data_not_readthrough.append(line_list)

    write_TSV(result_tmp_data_not_readthrough, output_file)
    write_TSV(result_tmp_data_readthrough, readthrough_output_file)


def read_TSV(tsv_file, read_from_string=False):
    if read_from_string:
        tsv_data_lines = tsv_file.rstrip('\n').split('\n')
        tsv_data_list = [line.split('\t') for line in tsv_data_lines]
        return tsv_data_list
    else:
        with open(tsv_file) as data_reader:
            tsv_data_list = [line.rstrip('\n').split('\t') for line in data_reader]
        return tsv_data_list


def write_TSV(result, out_file="result.txt", write_to_string=False):
    if write_to_string:
        result_tsv = '\n'.join(['\t'.join(line) for line in result])
        return result_tsv
    else:
        with open(out_file, 'w') as data_writer:
            for line in result:
                print('\t'.join(map(str, line)), file=data_writer)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-tmp", "--result_tmp_file", dest="result_tmp_file", help="[Project].result.tmp")    
    parser.add_argument("-o", "--output", dest="output", help="The output filename.")
    parser.add_argument("-ro", "--readthrough_output", dest="readthrough_output", help="The output filename for readthrough.")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    get_readthrough(args.result_tmp_file, args.output, args.readthrough_output)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import os
import pandas as pd
from glob import glob
import gzip

def main():

    # Args
    global args
    args = {}
    args['in_pattern'] = 'tmp/coloc_180908/*/*/*/*/*/coloc.pp.tsv'
    args['outf'] = 'output/coloc_interim_180908.tsv.gz'

    # Make output dir
    if not os.path.exists('output'): os.mkdir('output')

    # Open output file
    with gzip.open(args['outf'], 'wt') as out_h:

        header = [
            'study_id',
            'variant_id',
            'source_id',
            'tissue',
            'biomarker',
            'n_variants',
            'pp_h0',
            'pp_h1',
            'pp_h2',
            'pp_h3',
            'pp_h4',
            'pp_h4_over_h3',
        ]
        out_h.write('\t'.join(header) + '\n')

        # Iterate over input files
        for inf in glob(args['in_pattern']):

            # Get experiment info
            info = parse_info_from_path(inf)

            # Get results
            results = parse_results(inf)

            # Write result
            out_h.write('\t'.join([str(x) for x in info + results]) + '\n')

def parse_results(inf):
    ''' Parses coloc results
    Args:
        inf (file): input path
    Returns:
        list
    '''
    with open(inf, 'r') as in_h:
        in_h.readline()
        nvars = int(in_h.readline().rstrip().split('\t')[1])
        h0 = float(in_h.readline().rstrip().split('\t')[1])
        h1 = float(in_h.readline().rstrip().split('\t')[1])
        h2 = float(in_h.readline().rstrip().split('\t')[1])
        h3 = float(in_h.readline().rstrip().split('\t')[1])
        h4 = float(in_h.readline().rstrip().split('\t')[1])
        h4_over_h3 = h4 / h3
    return [nvars, h0, h1, h2, h3, h4, h4_over_h3]

def parse_info_from_path(inf):
    ''' Parses {study_id}/{variant_id}/{source_id}/{tissue}/{biomarker} from
        path.
    Args:
        inf (file): input path
    Returns:
        list
    '''
    info = os.path.dirname(inf).split('/')[-5:]
    return info

if __name__ == '__main__':

    main()

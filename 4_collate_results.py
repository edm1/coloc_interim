#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import os
import pandas as pd
from glob import glob
import gzip
import pandas as pd
import numpy as np

def main():

    # Args
    global args
    args = {}
    args['in_pattern'] = 'tmp/coloc_180908/*/*/*/*/*/coloc.pp.tsv'
    args['tissue_map'] = 'configs/tissue_codes.tsv'
    args['biomarker_map'] = 'configs/Sun_pQTL_SOMALOGIC_GWAS_protein_info.ensembl.manifest.tsv'
    args['outf'] = 'output/coloc_interim_180908.tsv.gz'

    # Load maps
    tissue_map = load_tissue_map(args['tissue_map'])
    gene_map = load_gene_map(args['biomarker_map'])

    # Make output dir
    if not os.path.exists('output'): os.mkdir('output')

    # Open output file
    with gzip.open(args['outf'], 'wt') as out_h:

        header = [
            'study_id',
            'variant_id',
            'source_id',
            'tissue_code',
            'tissue_name',
            'biomarker',
            'biomarker_gene',
            'n_variants',
            'pp_h0',
            'pp_h1',
            'pp_h2',
            'pp_h3',
            'pp_h4',
            'pp_h4_over_h3_log2',
        ]
        out_h.write('\t'.join(header) + '\n')

        # Iterate over input files
        for inf in glob(args['in_pattern']):

            # Get experiment info
            info = parse_info_from_path(inf)

            # Insert tissue name and gene ID
            info.insert(4, tissue_map[info[3]])
            info.insert(6, gene_map.get(info[5], info[5]))

            # Get results
            results = parse_results(inf)

            # Write result
            out_h.write('\t'.join([str(x) for x in info + results]) + '\n')


def load_tissue_map(inf):
    ''' Loads a tissue code -> tissue name map
    Args:
        inf (file): input file
    Returns:
        Dict
    '''
    d = {}
    with open(inf, 'r') as in_h:
        in_h.readline() # Skip header
        for line in in_h:
            tissue_name, _, tissue_code = line.rstrip().split('\t')
            d[tissue_code] = tissue_name.lower()
    return d

def load_gene_map(inf):
    ''' Loads a biomarker -> ensembl gene id map. This is currently only
        needed for uniprot IDs from Sun et al.
    Args:
        inf (file): input file
    Returns:
        Dict
    '''
    d = {}
    with open(inf, 'r') as in_h:
        in_h.readline() # Skip header
        for line in in_h:
            parts = line.rstrip().split('\t')
            uniprot = 'UNIPROT_' + parts[1].replace(',', '_')
            try:
                ensg = parts[5]
                d[uniprot] = ensg
            except IndexError:
                pass
    return d

def parse_results(inf):
    ''' Parses coloc results
    Args:
        inf (file): input path
    Returns:
        list
    '''
    with open(inf, 'r') as in_h:
        in_h.readline()
        nvars = int(float(in_h.readline().rstrip().split('\t')[1]))
        h0 = float(in_h.readline().rstrip().split('\t')[1])
        h1 = float(in_h.readline().rstrip().split('\t')[1])
        h2 = float(in_h.readline().rstrip().split('\t')[1])
        h3 = float(in_h.readline().rstrip().split('\t')[1])
        h4 = float(in_h.readline().rstrip().split('\t')[1])

        try:
            h4_over_h3_log = np.log2(h4 / h3)
        except ZeroDivisionError:
            h4_over_h3_log = np.log2(h4 / sys.float_info.min)

    return [nvars, h0, h1, h2, h3, h4, h4_over_h3_log]

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

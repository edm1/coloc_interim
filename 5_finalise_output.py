#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import os
import pandas as pd


def main():

    # Args
    global args
    args = {}
    args['inf'] = 'output/coloc_interim.full.tsv.gz'
    args['outf'] = 'output/coloc_interim.processed.tsv.gz'
    args['min_snps'] = 500

    # Load
    data = pd.read_csv(args['inf'], sep='\t', header=0)
    data = data.rename(columns={'biomarker_gene':'ensembl_id'})

    # Filter
    data = data.loc[data.n_variants >= args['min_snps'], :]

    # Sort
    data = data.sort_values(['study_id', 'variant_id', 'biomarker'])

    # Write
    data.to_csv(args['outf'], sep='\t', index=None, compression='gzip')



if __name__ == '__main__':

    main()

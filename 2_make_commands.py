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
    args['in_mani'] = 'configs/coloc_manifest_180908.csv'
    args['in_prot_map'] = 'configs/Sun_pQTL_SOMALOGIC_GWAS_protein_info.ensembl.manifest.tsv'
    args['in_tissue_map'] = 'configs/tissue_codes.tsv'
    args['coloc_window_kb'] = 500
    args['tmp_dir'] = 'tmp'

    # Make temp dir
    if not os.path.exists(args['tmp_dir']): os.mkdir(args['tmp_dir'])

    # Load manifest
    mani = load_manifest()
    mani = mani.loc[mani.chrom == '22', :].head(1) # DEBUG
    mani.to_csv('tmp/manifest_merged.tsv.gz', sep='\t', index=None, compression='gzip')



    return 0

def load_manifest():
    ''' Loads the manifest and merges required columns
    Returns:
        pd.Df
    '''
    # Load manifest
    mani = pd.read_csv(args['in_mani'], sep=',', header=0)
    mani['chrom'], mani['pos'], mani['ref'], mani['alt'] = \
        mani.index_variant_id.str.split('_').str
    mani.chrom = mani.chrom.astype(str)

    # Merge Sun pQTL uniprot
    soma = pd.read_csv(args['in_prot_map'], sep='\t', header=0)
    soma = soma.drop_duplicates(subset='ensembl_id')
    mani = pd.merge(mani, soma.loc[:, ['ensembl_id', 'UniProt']],
                    left_on='gene_id', right_on='ensembl_id',
                    how='left')

    # Merge tissue codes
    tissue = pd.read_csv(args['in_tissue_map'], sep='\t', header=0)
    tissue.prefix = tissue.prefix.str.lower()
    mani  = pd.merge(mani, tissue.loc[:, ['prefix', 'uberon_code']],
                    left_on='feature', right_on='prefix',
                    how='left')

    return mani

if __name__ == '__main__':

    main()

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
    # Input args
    args['in_mani'] = 'configs/coloc_manifest_180908.csv.gz'
    args['in_prot_map'] = 'configs/Sun_pQTL_SOMALOGIC_GWAS_protein_info.ensembl.manifest.tsv'
    args['in_tissue_map'] = 'configs/tissue_codes.tsv'
    # File patterns
    args['coloc_wrapper'] = 'scripts/coloc_wrapper.py'
    args['bgen'] = 'input_data/uk10k/bgen/{chrom}.ALSPAC_TWINSUK.maf01.beagle.anno_updated.csq.shapeit.20131101.bgen'
    args['disease'] = 'input_data/gwas/genome_wide/{study_id}/{trait_id}/{chrom}-{study_id}-{trait_id}.tsv.gz'
    args['eqtl'] = 'input_data/molecular_qtl/eqtl/GTEX7/{tissue}/{biomarker}/{chrom}-GTEX7-{tissue}-{biomarker}.tsv.gz'
    args['pqtl'] = 'input_data/molecular_qtl/pqtl/SUN2018/{tissue}/{biomarker}/{chrom}-SUN2018-{tissue}-{biomarker}.tsv.gz'
    args['out_pref'] = 'tmp/coloc_180908/{study_id}/{variant_id}/{source_id}/{tissue}/{biomarker}'
    # args['out_pref'] = 'output/coloc_180908/{study_id}/{study_id}-{variant_id}-{source_id}-{tissue}-{biomarker}'
    # Coloc args
    args['coloc_window_kb'] = 500
    # Other args
    args['tmp_dir'] = 'tmp'

    # Make temp dir
    if not os.path.exists(args['tmp_dir']): os.mkdir(args['tmp_dir'])

    # Load manifest
    mani = load_manifest()
    mani = mani.loc[mani.chrom == '22', :].head(1) # DEBUG
    mani.to_csv(args['tmp_dir'] + '/manifest_merged.tsv.gz', sep='\t',
                index=None, compression='gzip')

    # Make commands
    commands = mani.apply(make_commands, axis=1)
    commands.to_csv(args['tmp_dir'] + '/commands.txt.gz',
                    sep='\t',
                    index=None,
                    compression='gzip')
    # for command in commands:
    #     print(command)

    return 0

def make_commands(row):
    ''' Makes command to run coloc using wrapper
    Args:
        row (pd.Series)
    Returns:
        str containing shell command
    '''
    # Make input path names
    in_bgen = os.path.abspath(args['bgen'].format(
        chrom=row.chrom))
    in_disease_ss = os.path.abspath(args['disease'].format(
        study_id=row.stid,
        trait_id=row.stid.replace('NEALEUKB', 'UKB'),
        chrom=row.chrom))

    if row.source_id == 'gtex_v7':
        in_mol_ss = os.path.abspath(args['eqtl'].format(
            tissue=row.uberon_code,
            biomarker=row.gene_id,
            chrom=row.chrom))
        outf = os.path.abspath(args['out_pref'].format(
            study_id=row.stid,
            tissue=row.uberon_code,
            biomarker=row.gene_id,
            variant_id=row.index_variant_id,
            source_id=row.source_id,
            chrom=row.chrom))

    elif row.source_id == 'sun2018':
        in_mol_ss = os.path.abspath(args['pqtl'].format(
            tissue=row.uberon_code,
            biomarker=row.UniProt,
            chrom=row.chrom))
        outf = os.path.abspath(args['out_pref'].format(
            study_id=row.stid,
            tissue=row.uberon_code,
            biomarker=row.UniProt,
            variant_id=row.index_variant_id,
            source_id=row.source_id,
            chrom=row.chrom))

    else:
        sys.exit('Error: source_id {0} not recognised'.format(row.source_id))

    # Temp dir
    # out_tmp = os.path.abspath(
    #     args['tmp_dir'] + '/coloc_wrapper/{study_id}/'.format(
    #         study_id=row.stid))

    # Make command
    cmd = [
        'python',
        os.path.abspath(args['coloc_wrapper']),
        '--left_sumstats', in_disease_ss,
        '--right_sumstats', in_mol_ss,
        '--bgen', in_bgen,
        '--outpref', outf,
        '--pos', row.pos,
        '--window_kb', args['coloc_window_kb']
        # '--tmpdir', out_tmp
    ]

    return ' '.join([str(x) for x in cmd])

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

    # Depulicate
    mani = mani.drop_duplicates(subset=[
        'index_variant_id',
        'stid',
        'gene_id',
        'source_id',
        'feature'
        ])

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import os
import pandas as pd
from shutil import copyfile

def main():

    # Args
    inf = 'output/coloc_interim_180908.tsv.gz'
    plot_pattern = 'tmp/coloc_180908/{study_id}/{variant_id}/{source_id}/{tissue}/{biomarker}/coloc.plot.png'
    out_pattern = 'output/examples/{h}/{study_id}-{variant_id}-{source_id}-{tissue}-{biomarker}-coloc.plot.png'
    outdir = 'output/examples'
    hs = ['h{}'.format(x) for x in [0, 1, 2, 3, 4]]
    n_plots = 10

    # Make out dirs
    for h in hs:
        subdir = os.path.join(outdir, h)
        os.makedirs(subdir, exist_ok=True)

    # Load
    df = pd.read_csv(inf, sep='\t', header=0)
    # print(df.head())

    # for each hypothesis, find the highest PP and download N plots
    for h in hs:

        # Sort
        df_sort = df.sort_values('pp_{}'.format(h), ascending=False)

        # Take top N
        df_sort = df_sort.head(n_plots)

        # Make
        for i, row in df_sort.iterrows():

            # Make file names
            in_plot = plot_pattern.format(
                study_id=row['study_id'],
                variant_id=row['variant_id'],
                source_id=row['source_id'],
                tissue=row['tissue'],
                biomarker=row['biomarker']
            )
            out_plot = out_pattern.format(
                h=h,
                study_id=row['study_id'],
                variant_id=row['variant_id'],
                source_id=row['source_id'],
                tissue=row['tissue'],
                biomarker=row['biomarker']
            )

            # Copy
            copyfile(in_plot, out_plot)


if __name__ == '__main__':

    main()

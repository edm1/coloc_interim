#!/usr/bin/env bash
#

set -euo pipefail

mkdir -p input_data

# Download molecular qtl summary stats
# mkdir -p input_data/molecular_qtl
# gsutil -m rsync -rn gs://genetics-portal-sumstats/molecular_qtl input_data/molecular_qtl

# Download disease (GWAS) summary stats
# mkdir -p input_data/gwas
# gsutil -m rsync -rn gs://genetics-portal-sumstats/gwas input_data/gwas

# Download UK10K
mkdir -p input_data/uk10k
gsutil -m rsync -r gs://genetics-uk10k2-private input_data/uk10k

echo COMPLETE

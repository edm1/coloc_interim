#!/usr/bin/env bash
#

set -euo pipefail

mkdir -p input_data
cd input_data

gsutil -m rsync -rn gs://genetics-portal-sumstats/molecular_qtl molecular_qtl


echo COMPLETE

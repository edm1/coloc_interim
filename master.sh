#!/usr/bin/env bash
#

set -euo pipefail

# Args
instance_name="em-coloc-test"
instance_zone="europe-west1-d"

# Run
# bash 1_get_input_data.sh
# python 2_make_commands.py
bash 3_run_commands.sh
python 4_collate_results.py

# Tar the tmp dir
tar -czvf output/coloc_interim_tempdir_180908.tar.gz tmp

# Shutdown instance
gcloud compute instances stop $instance_name --zone=$instance_zone

echo COMPLETE

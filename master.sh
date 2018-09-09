#!/usr/bin/env bash
#

set -euo pipefail

#bash 1_get_input_data.sh
python 2_make_commands.py
bash 3_run_commands.sh
python 4_collate_results.py

echo COMPLETE

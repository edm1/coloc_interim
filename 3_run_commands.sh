#!/usr/bin/env bash
#
# Run all coloc commands in parallels
#

set -euo pipefail

cores=4
in_commands=tmp/commands.txt.gz

zcat < $in_commands | head -10 | while read cmd
do
    # Parse outfiles
    outfile=$(echo $cmd | cut -f 10 -d " ")/COMPLETE
    # If COMPLETE file does not exist, run command
    if [ ! -f $outfile ]; then
        echo $cmd
    fi
done | parallel -j $cores

echo COMPLETE

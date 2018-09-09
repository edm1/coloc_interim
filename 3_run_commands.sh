#!/usr/bin/env bash
#
# Run all coloc commands in parallels
#

set -euo pipefail

# Args
cores=96
in_commands=tmp/commands.txt.gz

echo START...

zcat < $in_commands | while read cmd
do
    # Parse outfiles
    outfile=$(echo $cmd | cut -f 10 -d " ")/COMPLETE
    # If COMPLETE file does not exist, run command
    if [ ! -f $outfile ]; then
        echo $cmd
    fi
done | parallel -j $cores

echo COMPLETE

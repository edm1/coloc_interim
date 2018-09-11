#!/usr/bin/env bash
#
# Run all coloc commands in parallels
#

set -euo pipefail

# Args
cores=64
in_commands=tmp/commands.txt.gz

echo START...

# Remove log files
rm -f tmp/commands.processing.log.txt.gz
rm -f tmp/commands.already_complete.log.txt.gz

zcat < $in_commands | while read cmd
do
    # Parse outfiles
    outfile=$(echo $cmd | cut -f 10 -d " ")/COMPLETE
    # If COMPLETE file does not exist, run command
    if [ ! -f $outfile ]; then
        echo $cmd | gzip -c >> tmp/commands.processing.log.txt.gz
        echo $cmd
    else
        echo $cmd | gzip -c >> tmp/commands.already_complete.log.txt.gz
    fi
done | parallel -j $cores

echo COMPLETE

#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "extract-wordlist.sh source.json"
    echo "Example extract-wordlist.sh yanbian-2009.json"
    exit 1;
fi
set -x
basename =$(basename $1)
prefix=${basename/%.json}
python ../utils/count_freq.py $1 $prefix-wordlist.txt
python ../utils/freq_filter.py $prefix-wordlist.txt $prefix-processed-wordlist.txt ../utils/virtual-word.filter
python ../utils/freq_filter.py $prefix-processed-wordlist.txt $prefix-foreign-wordlist.txt ../utils/foreign-word.filter

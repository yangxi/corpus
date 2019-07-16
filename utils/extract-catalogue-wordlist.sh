#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "extract-catalogue-worlist.sh source.json"
    echo "Example extract-wordlist.sh yanbian-2009.json"
    exit 1;
fi
set -x
filename=$(basename $1)
prefix=${filename/%.json}

python ../utils/content_filter.py $1 catalogue catalogue-$prefix
for cf in `ls ./catalogue-$prefix-*.json`; do
    cf_prefix=${cf/%.json}
    echo "Building word table for $cf";
    python ../utils/count_freq.py $cf $cf_prefix-wordlist.txt
    echo "Filtering virtual words from the table"
    python ../utils/freq_filter.py ${cf_prefix}-wordlist.txt ${cf_prefix}-processed-wordlist.txt ../utils/virtual-word.filter
    echo "Matching foreign words with the processed word table."
    python ../utils/freq_filter.py ${cf_prefix}-processed-wordlist.txt ${cf_prefix}-foreign-wordlist.txt ../utils/foreign-word.filter
done


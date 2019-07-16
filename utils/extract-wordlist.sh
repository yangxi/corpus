#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "extract-wordlist.sh source.json number-of-article"
    echo "Example extract-wordlist.sh yanbian-2009.json 20"
    exit 1;
fi
set -x
prefix=${1/%.json}
echo "python ../utils/content_filter.py $1 $2 $prefix-$2-article.json"
python ../utils/content_filter.py $1 $2 $prefix-$2-article.json
echo "python ../utils/count_freq.py $prefix-$2-article.json $prefix-$2-wordlist.txt"
python ../utils/count_freq.py $prefix-$2-article.json $prefix-$2-wordlist.txt
echo "python ../utils/freq_filter.py $prefix-$2-wordlist.txt $prefix-$2-processed-wordlist.txt ../utils/tags.txt"
python ../utils/freq_filter.py $prefix-$2-wordlist.txt $prefix-$2-processed-wordlist.txt ../utils/tags.txt

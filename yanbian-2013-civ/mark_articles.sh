#!/bin/bash
i=0
for url in `cat ./yanbian-2013-p176-p181.json | jq -r '.[].url'`; do
    echo "Process page $url";
    python ../utils/mark_yanbian.py $url $i.txt
    (( i=i+1 ))
    done

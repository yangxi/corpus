#!/bin/bash
i=0
for url in `cat $1 | jq -r '.[].url'`; do
    echo "Process page $url";
    python ../utils/mark_yanbian.py $url $i.txt
    (( i=i+1 ))
    done

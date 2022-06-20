#!/bin/bash
if [ -z "$1" ]; then
    echo "Run this command in the corpus directory"
    echo "./utils/fetch-and-parse.sh data-directory"
    exit 1
fi

if [ ! -d "./$1" ]; then
    echo "Missing data directory $1"
    echo "Please create on with mkdir $1"
    exit 1
fi

if [ ! -f "./$1/source.task" ]; then
    echo "Missing ./$1/source.task, please create one"
    exit 1
fi

if [ ! -f "./$1/source.json" ]; then
    echo "Crawling the data"
    cd ./crawler/yanbian
    scrapy crawl yanbian -a task=../../$1/source.task -o ../../$1/source.json | tee -a ../../$1/crawl.stdout
    cd ../..
fi


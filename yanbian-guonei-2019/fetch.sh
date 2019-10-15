#!/bin/bash
#cd ../crawler/yanbian
#echo "Crawling the data"
#scrapy crawl yanbian -a task=../../yanbian-guonei-2019/source.task -o ../../yanbian-guonei-2019.json
#cd ../../yanbian-guonei-2019
echo "Parsing the data"
./mark_articles.sh ./yanbian-guonei-2019.json > parsing.log
echo "Generate the summary"
python ../utils/count_tag.py *.txt > yanbian-guonei-summary.csv


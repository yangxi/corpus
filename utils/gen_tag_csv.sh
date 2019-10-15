#!/usr/bin/env bash

outputfile=`ls ./*.txt`
echo "url\ttitle\tTotalKorean\tEnglishRoot\tChineseRoot\tKoreanRoot\tEnglishRootList\tChineseRootList"
for i in `cat outputfile`; do

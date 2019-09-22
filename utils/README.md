* Usage
Extract word frequencies from the text source:
`python ../utils/count_freq.py ../data/yanbian-2019-1-9.json ./yanbian-2019-1-9-wordlist.txt`

Filter out the suffix josa and verb suffixes:
`python ../utils/freq_filter.py ./yanbian-2019-1-9-wordlist.txt ./yanbian-2019-1-9-nounlist.txt ../utils/pos-suffix.filter`

Generate per-catalgoue article list, extract  filter virtual workds, and match foreign words:
`../utils/extract-catalogue-wordlist.sh ./yanbian-2009.json`

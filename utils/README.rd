* Usage
Extract word frequencies from the text source:
`python ../utils/count_freq.py ./yanbian-2009.json ./yanbian-2009-wordlist.txt`

Filter out the virtual words:
`python ../utils/freq-filter.py ./yanbian-2009-wordlist.txt ./yanbian-2009-processed-wordlist.txt ../utils/virtual-word.filter`

Match foreign words with the wordlist:
`python ../utils/freq-filter.py ./yanbian-2009-processed-wordlist.txt ./yanbian-2009-foreign-wordlist.txt ../utils/foreign-word.filter`


Extract, filter virtual workds, and match foreign words:
`../utils/extract-wordlist.sh ./yanbian-2009.json`

Generate per-catalgoue article list, extract  filter virtual workds, and match foreign words:
`../utils/extract-catalogue-wordlist.sh ./yanbian-2009.json`

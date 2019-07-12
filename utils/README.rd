* Usage

Extract word frequencies from the text source.
`python ./count_freq.py ./yanbian-2009.json  ./yanbian-2009-freq-table.txt`

Filter out the virtual words which stored in the tags.txt
`python ./freq-filter.py ./yanbian-2009-freq-table.txt ./yanbian-2009-filtered-freq.txt ./tags.txt`

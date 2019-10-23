* usage

Crawling and parsing Yanbian webpages.

Create a new directory
`mkdir data-name`

Create a new task file `source.task` in the data directory:
`echo 'http://www.iybrb.com/news/60.html 1 1' > ./data-nme/source.task`

Crawl and parse the page
`./utils/crawl-and-parse.sh data-name`

Transform word lists
`python ./utils/excel_trans.py EXCEL_FILE`

Requirements:
pip install pandas
pip install xlrd
pip install openpyxl
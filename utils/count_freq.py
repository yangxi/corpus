import re
import sys
import json

def count_frequency(contents):
    freq = {}
    for article in contents:
        ks = article["content"]
        words = re.sub(r'([^\w]|[\d_])+', ' ', ks).strip().split(' ')
        for w in words:
            if w.strip() == "":
                continue
            if w in freq:
                freq[w]["count"] += 1
            else:
                freq[w]= {"count" : 1}
    return freq


def load_contents(fname):
    with open(fname, 'r') as sf:
        contents = json.load(sf)
        return contents
    return []

def report_frequency(freq, outfile):
    keys = list(freq.keys())
    keys.sort()
    with open(outfile, 'w') as wf:
        for k in keys:
            l = "{}\t{}\n".format(k, freq[k]["count"])
            wf.write(l)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("count_freq.py source dest")
        exit(1)
    source_file = sys.argv[1]
    contents = load_contents(source_file)
    freq = count_frequency(contents)
    report_frequency(freq, sys.argv[2])
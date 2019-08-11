import sys
import csv
from konlpy.tag import Okt

def remove_one_suffix(kw, tag):
    fw = kw
    for s in tag:
        pos = kw.find(s)
        if pos > 0 and len(s) + pos == len(kw):
            fw = kw[0:pos]
            return fw
    return fw

def remove_suffix(kw, tag):
    kw_len = len(kw)
    nw = kw
    while True:
        nw = remove_one_suffix(kw, tag)
        if (nw == kw):
            return nw
        #if len(nw) <= kw_len - 4:
        #    return nw
        kw = nw

def remove_pos_suffix(kw, suffix_tags):
    tags = Okt().pos(kw)
    ret = ""
    i = len(tags) - 1
    while i > 0:
        if tags[i][1] not in suffix_tags:
            for s in range(0, i + 1):
                ret += tags[s][0]
            break
        i = i-1
    return ret

def suffix_filter(freq, filter):
    """
    :param freq: dict [korean_word]:{freq:number
    :param tag: dict [korean_suffix_word]
    :return: freq: dict [korean_wrod]:{freq: number, from:[korean_works]}
    """
    ret = {}
    tag = filter["tags"]
    for kw in freq:
        c = freq[kw]["count"]
        fw = kw
        fw = remove_suffix(kw, tag)
        if fw in ret:
            ret[fw]["count"] += c
        else:
            ret[fw]= {"count": c, "from":[]}
        if fw != kw:
            ret[fw]["from"].append(kw)
    print(ret)
    return ret


def pos_filter(freq, filter):
    """
    :param freq: dict [korean_word]:{freq:number
    :param tag: dict [korean_suffix_word]
    :return: freq: dict [korean_wrod]:{freq: number, from:[korean_works]}
    """
    ret = {}
    tag = filter["tags"]
    for kw in freq:
        c = freq[kw]["count"]
        fw = kw
        fw = remove_pos_suffix(kw, tag)
        if fw in ret:
            ret[fw]["count"] += c
        else:
            ret[fw]= {"count": c, "from":[]}
        if fw != kw:
            ret[fw]["from"].append(kw)
    print(ret)
    return ret

def parse_freq_file(fname):
    ret = {}
    with open(fname) as f:
        for line in f:
            t = line.rstrip().split('\t')
            kw = t[0]
            kc = int(t[1])
            if kw in ret:
                print('Warning: {} is duplicated'.format(kw))
            ret[kw] = {"count":kc}
    return ret

def parse_virtual_word_filter(f):
    filter = {"name":"virtual word filter",
              "filter": suffix_filter,
              "tags":{}}
    tag_string = tag_file.read().strip()
    tags = parse_suffix_tag(tag_string)
    if tags:
        filter["tags"] = tags
    return filter

def parse_pos_filter(f):
    filter = {"name":"pos word filter",
              "filter": pos_filter,
              "tags":{}}
    tag_string = tag_file.read().strip()
    types = tag_string.split(' ')
    tags = {}
    for t in types:
        tags[t] = True
    if tags:
        filter["tags"] = tags
    return filter

def parse_foreign_word_filter(f):
    filter = {"name":"virtual word filter",
              "filter": match_filter,
              "tags":[]}
    tags = {}
    for l in f.readlines():
        w = l.strip()
        if w and w not in tags:
            tags[w] = True
    filter["tags"] = tags
    return filter

def match_filter(freq, filter):
    ret = {}
    tags = filter["tags"]
    for tag in tags.keys():
        ret[tag] = []
        for kw in freq.keys():
            if kw.find(tag) != -1:
                ret[tag].append({kw:freq[kw]})
    return ret

def report_match_filter(table, file):
    keys = list(table.keys())
    keys.sort()
    keys = sorted(keys, key=lambda key: 0 if (len(table[key]) == 0) else 1)

    with open(file, 'w') as f:
        for k in keys:
            line = "{}\t".format(k)
            #[{w:{from:[], count;x}}, ...}
            for m in table[k]:
                w = list(m.keys())[0]
                count = m[w]["count"]
                line += "{}\t{}\t".format(w, count)
            f.write(line+"\n")

def parse_suffix_tag(tag_string):
    t = tag_string.strip().split(",")
    ret = {}
    for k in t:
        ret[k] = True
    return ret

def report_txt_freq(freq, file_name):
    keys = list(freq.keys())
    keys.sort()
    with open(file_name, 'w') as txt_file:
        for k in keys:
            count = freq[k]["count"]
            from_list = freq[k]["from"]
            txt_file.write("{}\t{}\t{}\n".format(k, count, from_list))
def report_csv_freq(freq, csv_file):
    keys = list(freq.keys())
    keys.sort()
    with open(csv_file, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['word', 'count', 'from'])
        for k in keys:
            count = freq[k]["count"]
            from_list = freq[k]["from"]
            row = [k, count, from_list]
            filewriter.writerow(row)

if __name__ == '__main__':
    #"는,은,도,이,가,나,를,을,과,와,의,지,져,자,고,까,에,게,겠,서,적,더,데,히,여,려,면,로,러,라,다,뿐,니,해,했,졌,었,였,았,됐,되,된,한,할,하다,하기,하지,하는,하고,하던,하면,으로,보다,처럼,부터,까지"
    if len(sys.argv) != 4:
        print("freq_filter.py source target filter")
    else:
        freq_table = parse_freq_file(sys.argv[1])
        filter
        with open(sys.argv[3], 'r') as tag_file:
            first_line = tag_file.readline()
            if first_line.find("virtual word filter") != -1:
                print("Found one virtual worc filter")
                filter = parse_virtual_word_filter(tag_file)
                new_table = filter["filter"](freq_table, filter)
                report_txt_freq(new_table, sys.argv[2])
            elif first_line.find("foreign word filter") != -1:
                filter = parse_foreign_word_filter(tag_file)
                new_table = filter["filter"](freq_table, filter)
                report_match_filter(new_table, sys.argv[2])
            elif first_line.find("pos suffix filter") != -1:
                filter = parse_pos_filter(tag_file)
                new_table = filter["filter"](freq_table, filter)
                report_txtfreq(new_table, sys.argv[2])


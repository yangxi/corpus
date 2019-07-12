import sys
import csv

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

def suffix_filter(freq, tag):
    """
    :param freq: dict [korean_word]:{freq:number
    :param tag: dict [korean_suffix_word]
    :return: freq: dict [korean_wrod]:{freq: number, from:[korean_works]}
    """
    ret = {}
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
        print("freq_filter.py source target tags")
    else:
        freq_table = parse_freq_file(sys.argv[1])
        tags = {}
        with open(sys.argv[3], 'r') as tag_file:
            tag_string = tag_file.read().strip()
            tags = parse_suffix_tag(tag_string)
        print(tags)
        new_table = suffix_filter(freq_table, tags)
        report_txt_freq(new_table, sys.argv[2])

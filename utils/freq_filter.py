import sys
import csv
import os
import json
from konlpy.tag import Okt
from utils import search_kw
import time

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
    if '' in ret:
        del ret['']
    return ret


def dict_filter(freq, filter):
    ret = {}
    k_dict = filter["dict"]
    search_log_file = None
    if "search_log" in filter["dict_filter"]:
        search_log_path = os.path.expanduser(filter["dict_filter"]["search_log"])
        search_log_file = open(search_log_path, 'a+')
        print("Open search_log_file {}".format(search_log_path))

    for kw in freq:
        if kw in ret:
            continue
        c = freq[kw]["count"]
        if kw not in k_dict:
            try:
                def block_callback():
                        if filter["dirty"] and filter["update"]:
                            print("Update Filter in the call back.")
                            update_dict(filter)
                kw_result = search_kw(kw, True, block_callback, search_log_file)
                print("Add a word to dict", kw_result)
                k_dict[kw] = kw_result
                filter["dirty"] = True
            except Exception as e:
                print("Received one exception", e)
                break
        k = k_dict[kw]
        ret[kw] = {"count":c, "dict":k}
    if filter["dirty"] and filter["update"]:
        print("Update Filter")
        update_dict(filter)
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
            ret[kw] = {"count":kc, "line":line}
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

def load_dict_file(f):
    dict = {}
    if not os.path.exists(f):
        with open(f, 'w') as dictfile:
            dictfile.write(json.dumps(dict))
    with open(f, 'r') as dictfile:
        dict = json.load(dictfile)
    return dict

def update_dict(filter):
    dict_file = os.path.expanduser(filter["dict_filter"]["dict_file"])
    with open(dict_file, 'w') as df:
        df.write(json.dumps(filter["dict"]))
    

def parse_dict_filter(f):
    filter = {
        "name":"dictionary",
        "filter": dict_filter,
        "dirty": False,
        "update": True,
        "report": report_txt_dict
        }
    dict_string = tag_file.read().strip()
    dict_json = json.loads(dict_string)
    if "dict_file" not in dict_json:
        raise "The Dict filter {} does not have the dict field.".format(dict_string)
    if "update" in dict_json:
        filter["update"] = dict_json["update"]
    filter["dict_filter"] = dict_json
    # load the dict
    filter["dict"] = load_dict_file(os.path.expanduser(dict_json["dict_file"]))
#    print(filter)
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

def dict_entry_to_string(kd):
    #{'word': '가능성', 'char': 'ko', 'explain': '가능성', 'from': 'zh', 'from_word': '可能性'}
    # -> ko 가능성 zh 可能性
    ret = ""
    for k in ["char", "from", "explain", "from_word"]:
        if k in kd:
            ret += "{}\t".format(kd[k])
        else:
            ret += " \t"
    return ret

def report_txt_dict(wl, file_name):
    keys = list(wl.keys())
    keys.sort()
    with open(file_name, 'w') as txt_file:
        for k in keys:
            count = wl[k]["count"]
            l = "{}\t{}\t".format(k, count)
            if 'dict' in wl[k]:
                l += dict_entry_to_string(wl[k]['dict'])
            txt_file.write(l+"\n")

# report the virtual filter
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
                report_txt_freq(new_table, sys.argv[2])
            elif first_line.find("dict filter") != -1:
                filter = parse_dict_filter(tag_file)
                new_table = filter["filter"](freq_table, filter)
                filter["report"](new_table, sys.argv[2])




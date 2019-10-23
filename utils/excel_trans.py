from pandas import DataFrame, read_csv
import pandas as pd
import ast
import os
import sys


def load_excel(file, sheet=None):
    # read the first one,
    if sheet:
        return pd.read_excel(file, sheet)
    else:
        return pd.read_excel(file)

def merge_word_list(list, key):
    thelist = []
    wl = list[1:]
    for r in wl:
        if r and str(r).startswith('['):
            r = str(r)
            words = ast.literal_eval(r)
            for w in words:
                thelist.append(w)
    return DataFrame({key: thelist})

def trans_word_list(list, key_prefix):
    w_col = {}
    max_line = 0
    for i in range(1, len(list)):
        r = list[i]
        if r and str(r).startswith('['):
            r = str(r)
            c = ast.literal_eval(r)
            if len(c) > max_line:
                max_line = len(c)
            c_name = "{}_{}".format(key_prefix, i)
            w_col[c_name] = c
    for i in w_col:
        r = w_col[i]
        if len(r) < max_line:
            for i in range(0, max_line - len(r)):
                r.append('')
    return DataFrame(w_col)
def trans_file(file):
    full_path = os.path.expanduser(file)
    exl = load_excel(full_path)
    if 'EnglishRootList' in exl and 'ChineseRootList' in exl:
        merged_eng_list = merge_word_list(exl["EnglishRootList"], 'AllEnglishRootList')
        transed_ch_list = trans_word_list(exl["ChineseRootList"], 'article')
        writer = pd.ExcelWriter(full_path, mode='a')
        merged_eng_list.to_excel(writer, 'EnglishRootList')
        transed_ch_list.to_excel(writer, 'ChineseRootList')
        writer.save()
        print(merged_eng_list)
        print(transed_ch_list)

if __name__ == '__main__':
    usage="python excel_trans.py excel_file"
    if len(sys.argv) < 2:
        print(usage)
        exit(1)
    else:
        for i in sys.argv[1:]:
            print("Transform Excel file {}".format(i))
            trans_file(i)

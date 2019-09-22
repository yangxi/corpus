import sys
import json
import os
import ast

def add(dict_file, add_file):
    k_dict = {}
    with open(dict_file,'r') as df:
        k_dict = json.load(df)
        print("Dict has {} words".format(len(k_dict.keys())))
    with open(add_file, 'r') as f:
        for l in f.readlines():
#            d = json.loads(l)
            l = l.strip()
            if l == "":
                continue
            d = ast.literal_eval(l)
            if "word" not in d:
                print("Unknown ling: {}".format(l))
                continue
            d_w = d["word"]
            if d["word"] not in  k_dict:
                print("Add word {}".format(d["word"]))
                k_dict[d_w] = d
            else:
                print("{} in the dict already.".format(d_w))
                k_dict[d_w] = d
    #re-write k_dict
    with open(dict_file, 'w') as df:
        df.write(json.dumps(k_dict))

def delete(dict_file, delete_file):
    k_dict = {}
    with open(dict_file,'r') as df:
        k_dict = json.load(df)
        print(k_dict)
    with open(delete_file, 'r') as f:
        for l in f.readlines():
#            d = json.loads(l)
            d = ast.literal_eval(l)
            d_w = d["word"]
            if d["word"] in k_dict:
                print("Delete word {}".format(d["word"]))
                del k_dict[d_w]
            else:
                print("Cannot find {} in the dict.".format(d_w))
    #re-write k_dict
    with open(dict_file, 'w') as df:
        df.write(json.dumps(k_dict))

def report(dict_file):
    k_dict = {}
    with open(dict_file,'r') as df:
        k_dict = json.load(df)
        for k in k_dict:
            str = "{}\t".format(k)
            d = k_dict[k]
            print(d)
            for i in ["char","from","explain","from_word"]:
                if i in d:
                    str += "{}\t".format(d[i])
                else:
                    str += "{}\t".format(" ")
            print(str)

if __name__ == "__main__":
    if sys.argv[1] == 'delete' and len(sys.argv) == 4:
        delete(os.path.expanduser(sys.argv[2]), os.path.expanduser(sys.argv[3]))
    elif sys.argv[1] == 'add' and len(sys.argv) == 4:
        add(os.path.expanduser(sys.argv[2]), os.path.expanduser(sys.argv[3]))
    elif sys.argv[1] == "report":
        report(os.path.expanduser(sys.argv[2]))


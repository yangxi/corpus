import datetime
import os
import json
from bs4 import BeautifulSoup
import requests
from utils import char_type_detect



class NaverDict:
    kr_dict = {}
    dict_file = None
    dict_dirty = False
    search_log = None
    blocked = False
    def __init__(self, dictFile="~/naver-kr.json", searchLog="~/naver-search.log"):
        self.dict_file = os.path.expanduser(dictFile)
        self.kr_dict = self.load_dict()
        self.search_log = open(os.path.expanduser(searchLog),'a')

    def load_dict(self):
        if os.path.exists(self.dict_file):
            with open(self.dict_file, 'r') as df:
                new_dict = json.load(df)
                if type(new_dict) != dict:
                    return {}
                else:
                    return new_dict
        else:
            return {}
        print("Load Naver Kr dict from {} with {} entries".format(self.dict_file, len(list(self.dict_file.keys()))))
    def save_dict(self):
        with open(self.dict_file, 'w') as df:
            df.write(json.dumps(self.kr_dict))
            self.dict_dirty = False
    def parser_naver_html(self, kw, naver_page = None):
        if naver_page == None:
            if self.blocked == True:
                now = datetime.datetime.now()
                if now >= self.unblocked_time:
                    self.blocked = False
                    self.blocked_time = None
                    self.unblocked_time = None
                else:
                    raise Exception("Service is blocked until {}".format(self.unblocked_time))
            url = "https://dict.naver.com/search.nhn?dicQuery={}".format(kw)
            r = requests.post(url, timeout=5)
            if (r.text.find('Service access is temporarily blocked') != -1):
                self.blocked = True
                self.blocked_time = datetime.datetime.now()
                self.unblocked_time = self.blocked_time + 1 * datetime.datetime.hour
                raise Exception("Service is blocked until {}".format(self.unblocked_time))
            naver_page = r.text
        ret = []
        t = BeautifulSoup(naver_page, 'html.parser')
        kr_dict = t.find('div',{"class":"kr_dic_section"})
        if kr_dict == None:
            return None
        print("Found kr_dict section")
        kr_lst = kr_dict.find('ul',{"class":"lst_krdic"})
        if kr_lst == None:
            return None
        kr_lst = kr_lst.find_all('li')
        if len(kr_lst) == 0:
            return None
        print("Found kr_dict list: {}".format(len(kr_lst)))
        for e in kr_lst:
            # [{"word":kr, "explain":exp, "root":(root.text, root_type)}]
            d = {}
            exp = e.find_all('p')
            title = exp[0]
            explain = exp[1]
            word = title.find('span',{"class":"c_b"})
            if word == None:
                continue
            word_type = char_type_detect(word.text)
            d["word"] = (word.text, word_type)
            if explain:
                d["explain"] = explain.text.strip()
            else:
                d["explain"] = ""
            root = title.find('span', {"class":"word_class"})
            if root:
                print("Found word_class")
                root_type = char_type_detect(root.text)
                if root_type != 'en':
                    print("WARN: {} is not English".format(root.text))
                d["root"] = (root.text, root_type)
            else:
                root = title.find('span', {"class": "word_class2"})
                if root:
                    print("Found word_class2")
                    root_type = char_type_detect(root.text)
                    if root_type != 'zh':
                        print("WARN: {} is not Chinese".format(root.text))
                    d["root"] = (root.text, root_type)
            ret.append(d)
        return ret

    def search(self, kw):
        if kw in self.kr_dict:
            return self.kr_dict[kw]
        else:
            newWord = self.parser_naver_html(kw)
            if len(newWord) > 0:
                self.kr_dict[kw] = newWord
                self.dict_dirty = True
            return newWord
        # we have to search the Naverdict now.

    def dict_size(self, dict):
        return len(list(dict.keys()))

    def update(self, force=False):
        if force or self.dict_dirty:
            file_dict = self.load_dict()
            file_dict_size = self.dict_size(file_dict)
            mem_dict_size = self.dict_size(self.kr_dict)
            if force or mem_dict_size > file_dict_size:
                print("Plan to update in file dict from {} to {}".format(file_dict_size, mem_dict_size))
                self.save_dict()
            else:
                print("Avoid updating the in-file dict because In-memory dict({}) is not larger than in-file dict({}).".format(file_dict_size, mem_dict_size))
            #the dict must larger thant the file
    def self_check(self, update=False):
        for w in self.kr_dict:
            for e in self.kr_dict[w]:
                if 'root' in e:
                    root = e["root"]
                    root_type = char_type_detect(root[0])
                    if root_type != root[1]:
                        print("{}:{}".format(root[1], root_type))
                        print("{} root text does not agree with root type".format(e))
                        if update:
                            e["root"] = (root[0], root_type)
                            self.dict_dirty = True
        self.update()
#if __name__ == "__main__":
#    naver_kr = NaverDict("~/naver-kr.json")
#    naver_kr.update(True)

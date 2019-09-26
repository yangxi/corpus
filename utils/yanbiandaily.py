import os
import json
import requests
from bs4 import BeautifulSoup
import sys, traceback

class YanbianDaily:
    def __init__(self, yanbianpage="~/yanbian_daily.json"):
        self.page_file = os.path.expanduser(yanbianpage)
        self.pages = self.load_pages()
        self.pages_dirty = False

    def load_pages(self):
        if os.path.exists(self.page_file):
            with open(self.page_file, 'r') as df:
                pages = json.load(df)
                if type(pages) != dict:
                    return {}
                else:
                    return pages
        else:
            return {}

    def dict_size(self, dict):
        return len(list(dict.keys()))

    def get_tag_text(self, b, tag, cla=None, default=None):
        t = None
        if cla:
            t = b.find(tag, cla)
        else:
            t = b.find(tag)
        if t:
            return t.text.strip()
        else:
            return default
    def get_catalogue(self, r):
        mbx = r.find('div',{"class":"mbx"})
        if mbx:
            l = mbx.find_all('a')
            ret = []
            for c in l:
                ret.append(c.text)
            return ret
        else:
            cat = r.find('p',{"class":"select_cate"})
            if cat:
                return cat.text.strip()
            return ""
    def get_date(self, t):
        #try old style date first
        date_tag = self.get_tag_text(t, 'li', {"class":"letter"})
        if date_tag:
            return date_tag
        rlox = t.find('div',{"class":"rlox"})
        if rlox:
            return self.get_tag_text(rlox, 'p', default="")
        else:
            return ""
    def get_content(self, t):
        # try old first
        content = self.get_tag_text(t, 'div', {"id":"articleBody"})
        if content == None:
            return self.get_tag_text(t, 'div', {"class": "content"}, default="")
        else:
            return content

    # {"url":url, "title":title, "date":date, "content":content, "catalogue":catalogue}
    def get_page(self, url):
        p = requests.get(url, timeout=5)
        p.encoding = 'utf-8'
        html=p.text
        t = BeautifulSoup(p.text, 'html.parser')
        title = self.get_tag_text(t, 'title')
        catalogue = self.get_catalogue(t)
        date = self.get_date(t)
        content = self.get_content(t)
        return {"url":url, "title":title, "catalogue":catalogue,"date": date, "content":content, "html": html}

    def search_page(self, url):
        if url in self.pages:
            return self.pages[url]
        else:
            try:
                new_page = self.get_page(url)
                print("Got a newpage:{}", new_page)
                self.pages[url] = new_page
                self.pages_dirty = True
                return new_page
            except Exception as exp:
                print("Exception:{} while parsing url:{}".format(exp, url))
                traceback.print_exc(file=sys.stdout)
                return None
    def save_pages(self):
        with open(self.page_file, 'w') as df:
            df.write(json.dumps(self.pages))
            self.pages_dirty = False

    def update_pages(self, force=False):
        if force or self.pages_dirty:
            file_dict = self.load_pages()
            file_dict_size = self.dict_size(file_dict)
            mem_dict_size = self.dict_size(self.pages)
            if mem_dict_size >= file_dict_size or force:
                print("Update yanbian pages from {} to {}".format(file_dict_size, mem_dict_size))
                self.save_pages()




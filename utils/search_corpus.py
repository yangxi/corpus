import os
import json

from pandas import DataFrame
from utils.count_tag import TaggedArticle

class CorpusFrames:
    # row format
    # keys: corpus_source, corpus_source_file, tag_file, title, author, catalogue, date, summary url content
    corpus = {}
    corpus_frames = None
    corpus_source = ""
    corpus_path = ""
    
    # {source: str, tags: [str]}
    corpus_dir = {}
    # search all corpus direcotires and load the articles DIR/source.json ad the tags DIR/[0-9]*.txt
    def __init__(self, corpus_source, dir_path):
        fpath = dir_path
        if fpath.startswith("~"):
            fpath = os.path.expanduser(fpath)
        self.corpus_path = fpath
        self.corpus_source = corpus_source
        self.find_corpus_dirs(fpath)
        # we load the sources first, then reload the tag files
        for corpus_path in self.corpus_dir:
            self.load_corpus_sources(corpus_path)
        for corpus_path in self.corpus_dir:
            self.load_corpus_tags(corpus_path)
        self.generate_corpus_frames()

    def generate_corpus_frames(self):
        # get a collection of frames         
        columns = {}
        for i in self.corpus:
            art = self.corpus[i]
            if 'tag' in art:                
                # this should be a good example                
                for k in art:
                    if k == 'tag':
                        for tagk in art[k]:
                            if tagk not in columns:
                                columns[tagk] = []
                    else:
                        if k not in columns:
                            columns[k] = []        
                break     

        for i in self.corpus:
            added_keys = {}
            for k in columns:
                added_keys[k] = False
            art = self.corpus[i]
            for k in art:            
                if k == 'tag':
                    for tagk in art[k]:
                        v = art[k][tagk]
                        if tagk in columns and added_keys[tagk] == False:
                            columns[tagk].append(v)
                            added_keys[tagk] = True
                else:
                    v = art[k]
                    if k in columns and added_keys[k] == False:                        
                        columns[k].append(v)
                        added_keys[k] = True
            for k in added_keys:
                if added_keys[k] is False:
                    columns[k].append(None)
                    added_keys[k] = True
        self.corpus_frames = DataFrame.from_dict(columns)

    def find_corpus_dirs(self, dir_path):    
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file == "source.json":
                    print("Found one corpus directory: %s" %(root))
                    if root not in self.corpus_dir:
                        self.corpus_dir[root] = os.path.join(root, file)
    # source.json
    # DIR/source.json [{[title, autor, catalogue, date, img, summary, url, content]}]
    # DIR/0.txt, 1.txt...
    def load_corpus_sources(self, dir_path):        
        source_path = dir_path + "/source.json"
        if os.path.exists(source_path) == False:
            return        
        with open(source_path, 'r') as sf:
            articles = json.load(sf)
            print("Read %d articles in the source file %s." % (len(articles), source_path))
            for i in range(0, len(articles)):
                doc = articles[i]
                if doc['url'] not in self.corpus:
                    url = doc['url']
                    self.corpus[url] = doc
                    doc['corpus_source'] = self.corpus_source
                    doc['corpus_source_file'] = source_path                    
                    # load dir_path/0.txt
                    # tag_file = dir_path + "/{}.txt".format(i)
                    # tags = {}
                    # try:
                    #     tagarticle = TaggedArticle(tag_file)
                    #     tags = tagarticle.tag
                    # except Exception as taggingexp:
                    #     print("Exception when loading the article {} in the source file {}: {}".format(url, dir_path, taggingexp))
                    # doc['tags'] = tags            

    def load_corpus_tags(self, dir_path):
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.txt'):
                    # this could be a tag file
                    tag_file_path = os.path.join(root, f)
                    try:
                        tagarticle = TaggedArticle(tag_file_path)
                        tags = tagarticle.tag
                        tag_url = tags['url']
                        if tag_url in self.corpus:                            
                            article = self.corpus[tag_url]
                            if 'tag' in article:
                                print("Duplicated tag in the tag file {} in article {}".format(tag_file_path, article))
                            else:
                                article['tag_file'] = tag_file_path
                                article['tag'] = tags
                        else:
                            print("Tag {} in the tag file {} doesn't exist in the source corpus".format(tag_url, tag_file_path) )
                    except Exception as te:
                        print("Exceptionn when loading the tag file {}:{}".format(tag_file_path, te))
                    #     tags = tagarticle.tag
                    # except Exception as taggingexp:
                    #     print("Exception when loading the article {} in the source file {}: {}".format(url, dir_path, taggingexp))
                    # doc['tags'] = tags  
                        

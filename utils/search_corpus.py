import os
import json

from pandas import DataFrame
import pandas as pd
from utils.count_tag import TaggedArticle

class CorpusFrames:
    # search all corpus direcotires and load the articles DIR/source.json ad the tags DIR/[0-9]*.txt
    def __init__(self, corpus_source, dir_path):
        # row format
        # keys: corpus_source, corpus_source_file, tag_file, title, author, catalogue, date, summary url content
        self.corpus = {}
        self.corpus_frames = None
        self.corpus_source = ""
        self.corpus_path = ""
        self.empty_articles = 0
        self.corpus_dir = {}

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
        #turn the date column to datetime
        if 'date' in columns:
            self.corpus_frames.date = pd.to_datetime(self.corpus_frames.date)
            # sort by date
            self.corpus_frames = self.corpus_frames.sort_values(by='date')
            # reset the index
            self.corpus_frames = self.corpus_frames.reset_index(drop=True)

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
                    if 'content' in doc and doc['content'] == "":
                        self.empty_articles += 1
                        continue
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
                                print("Tag in tagfile:{} is duplicated in the article {} loaded from another tagfile:{}.\n ".format(tag_file_path, article['url'], article['tag_file']))
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
    def find_word(self, word, frames=None):
        source = frames if frames else self.corpus_frames
        hits = source[source.content.str.contains(word)]
        print("{} of {} ({:.2f}) has the word {}".format(hits.size, self.corpus_frames.size, hits.size*1.0 / self.corpus_frames.size, word))
        # iterate the hits
        output = ""
        for index, r in hits.iterrows():
            output += "\n==== id:{} date:{} title:{} catalogue:{}\n".format(index, r['date'], r['title'], r['catalogue'])
            # we output the matched sentences for each article
            sentences = r['content'].split('.')
            nr_s = 1
            for s in sentences:
                if s.find(word) > 0:
                    output += "\n{}:  {}\n".format(nr_s, s.replace('\r\n', "").strip())
                    nr_s += 1
        print(output)
        return hits

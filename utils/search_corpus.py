import os
import json

from pandas import DataFrame
import pandas as pd
import regex
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
        column_list = ['title', 'author', 'catalogue', 'date', 'summary', 'url', 'content',
        'corpus_source', 'corpus_source_file', 'tag_file', 'title_korean_words',
       'title_chinese_words', 'title_japaness_words', 'title_unknow_words',
       'title_total_words', 'title_kroot_words', 'title_croot_words',
       'title_eroot_words', 'title_oroot_words', 'title_korean_nouns',
       'title_kroot_nouns', 'title_croot_nouns', 'title_eroot_nouns',
       'title_oroot_nouns', 'title_korean_verbs', 'title_kroot_verbs',
       'title_croot_verbs', 'title_eroot_verbs', 'title_oroot_verbs',
       'title_eroot_list', 'title_croot_list', 'title_tag_text',
       'body_korean_words', 'body_chinese_words', 'body_japaness_words',
       'body_unknow_words', 'body_total_words', 'body_kroot_words',
       'body_croot_words', 'body_eroot_words', 'body_oroot_words',
       'body_korean_nouns', 'body_kroot_nouns', 'body_croot_nouns',
       'body_eroot_nouns', 'body_oroot_nouns', 'body_korean_verbs',
       'body_kroot_verbs', 'body_croot_verbs', 'body_eroot_verbs',
       'body_oroot_verbs', 'body_eroot_list', 'body_croot_list',
       'body_tag_text', 'article_korean_words', 'article_chinese_words',
       'article_japaness_words', 'article_unknow_words', 'article_total_words',
       'article_kroot_words', 'article_croot_words', 'article_eroot_words',
       'article_oroot_words', 'article_korean_nouns', 'article_kroot_nouns',
       'article_croot_nouns', 'article_eroot_nouns', 'article_oroot_nouns',
       'article_korean_verbs', 'article_kroot_verbs', 'article_croot_verbs',
       'article_eroot_verbs', 'article_oroot_verbs', 'article_eroot_list',
       'article_croot_list', 'article_tag_text', 'tag_file_path']
        columns = {}
        for k in column_list:
            columns[k] = []
        
        # for i in self.corpus:
        #     art = self.corpus[i]
        #     if 'tag' in art:                
        #         # this should be a good example                
        #         for k in art:
        #             if k == 'tag':
        #                 for tagk in art[k]:
        #                     if tagk not in columns:
        #                         columns[tagk] = []
        #             else:
        #                 if k not in columns:
        #                     columns[k] = []        
        #         break     

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
    def find_word(self, word, column="content",frames=None):
        source = frames if frames else self.corpus_frames
        col = source[column]
        hits = source[col.str.contains(word)]
        source_len = len(self.corpus_frames)
        hits_len = len(hits)
        print("{} of {} ({:.2f}) has the word {}".format(hits_len, source_len, (1.0 * hits_len) / source_len, word))
        # iterate the hits
        output = ""
        for index, r in hits.iterrows():
            output += "\n==== id:{} date:{} title:{} catalogue:{}\n".format(index, r['date'], r['title'], r['catalogue'])
            # we output the matched sentences for each article
            sentences = r[column].split('.')
            nr_s = 1
            for s in sentences:
                if s.find(word) > 0:
                    output += "\n{}:  {}\n".format(nr_s, s.replace('\r\n', "").strip())
                    nr_s += 1
        print(output)
        return hits

    def find_korean_words_with_prefix(self, prefix,  prefix_size= None, column="content", frames=None):
        regx =  str(prefix) + '\p{IsHangul}*'
        if prefix_size:
            regx = str(prefix) + r'\p{IsHangul}' + '{' + str(prefix_size) + '}'
        return self.re_find_word_in_content(regx, column, frames)

    def find_korean_words_with_suffix(self, suffix,  prefix_size= None, column="content", frames=None):
        regx = r'\p{IsHangul}*' + suffix
        if prefix_size:
            regx = r'\p{IsHangul}' + '{' + str(prefix_size) + '}' + suffix
        return self.re_find_word_in_content(regx, column, frames)

    def re_find_word_in_content(self, rexp, column="content", frames=None):
        source = frames if frames else self.corpus_frames
        col = source[column]
        hit_source = col.apply(lambda x: len(regex.findall(rexp, x.replace('\r\n','').strip())) > 0)
        hits = source[hit_source]
        source_len = len(self.corpus_frames)
        hits_len = len(hits)       
        # iterate the hits
        output = ""
        matched_words = {}
        for index, r in hits.iterrows():
            output += "\n==== id:{} date:{} title:{} catalogue:{}\n".format(index, r['date'], r['title'], r['catalogue'])
            # we output the matched sentences for each article
            sentences = r[column].split('.')    
            nr_s = 1
            for s in sentences:
                content = s.replace('\r\n', "").strip()
#                print("s.findall {} {}".format(r, content))
                words = regex.findall(rexp, content)                
                if len(words) > 0:                    
                    output += "\n{}, words:{}:  {}\n".format(nr_s, words, content)
                    nr_s += 1
                    for w in words:
                        if w not in matched_words:
                            matched_words[w] = True
        print("{} of {} ({:.2f}) has matched words {}".format(hits_len, source_len, (1.0 * hits_len) / source_len, list(matched_words.keys())))
        print(output)
        return hits

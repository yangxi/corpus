from utils.word_root import mark_article
import os, json

class CorpusAnalyzer:
    def __init__(self, corpus_source):
        self.articles = []
        if corpus_source.startswith("~"):
            corpus_source = os.path.expanduser(corpus_path)        
        self.corpus_source_file = corpus_source
        if os.path.exists(self.corpus_source_file):
            with open(self.corpus_source_file, 'r') as sf:
                self.articles = json.load(sf)

    # parse unparsed articles
    def tag_articles(self, all_articles = False):
        nr_tagged = 0
        total = 0
        nr_tag_error = 0
        for art in self.articles:
            if all_articles == True or 'tag' not in art:
                total += 1
        for art in self.articles:        
            if all_articles == True or 'tag' not in art:
                try:
                    print('(%d/%d) Tag article %s' % (nr_tagged, total, art['url']))                
                    tag = mark_article(art)
                    art['tag'] = tag
                    nr_tagged += 1
                except Exception as tagException:
                    nr_tag_error += 1
                    print("tag exception when processing article %s: %s" % (art['url'], tagException))
        print("Tag %d articles with %d errors" % (nr_tagged, nr_tag_error))
        
    def save_articles(self, dest):
        if dest.startswith("~"):
            dest = os.path.expanduser(dest)
        with open(dest, 'w') as df:
            df.write(json.dumps(self.articles))
            
# if __name__ == '__main__':
#     usage="python mark_corpus.py corpus_path"
#     # this command loads corpus_path/source.json, parse articles, and generate the output at corpus_path/ID.txt
#     if len(sys.argv) >= 2:
#         marker = MarkArticles(sys.argv[1])
#         marker.parse_articles()
#         marker.generate_tags()        
#     else:
#         print(usage)
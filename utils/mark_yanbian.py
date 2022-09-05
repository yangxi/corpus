import sys, os, json
from word_root import parse_line
from yanbiandaily import YawonbianDaily

class MarkArticles:
    def __init__(self, corpus_path):        
        self.articles = []
        self.corpus_path = corpus_path
        corpus_source_file = corpus_path + '/source.json'
        if os.path.exists(corpus_source_file):
            with open(corpus_source_file) as sf:
                self.articles = json.load(sf)
    def parse_articles(self):
        for i in range(0, len(self.articles)):
            # parse self.articles[i] and generate corpus_path/$i.txt
        # generate corpus_path/article.json
    def parse_article(self, article):
        title = article["title"]
        content = article["content"]
        tag_title = parse_line(title)
        tag_content = parse_line(content)
        article["yanbian_root_tag"] = {"title": tag_title, "content": tag_content}
        yanbian.pages_dirty = True
    tag_title = article["yanbian_root_tag"]["title"]
    tag_content = article["yanbian_root_tag"]["content"]
    yanbian.update_pages()
    if outputfile == None:
        outputfile = get_output_name(article)
    output = ""
    output += "url:{}\n".format(url)
    output += "=============================\n"
    output += get_root_usage(tag_title)
    output += tag_title["view"]
    output += "=============================\n"
    output += get_root_usage(tag_content)
    output += tag_content["view"]
    # output += "=============================\n"
    # output += "{}".format(tag_title)
    # output += "=============================\n"
    # output += "{}".format(tag_content)
    print(output)
    with open(outputfile,'w') as outf:
        print("Write the view to file:{}".format(outputfile))
        outf.write(output)
    def parse_article():

def get_output_name(article):
    catalogue = article["catalogue"]
    if type(catalogue) == list:
        catalogue = catalogue[-2]
    if catalogue == "":
        catalogue = "unknown"
    title = article["title"]
    date = article["date"]
    return "{}-{}-{}.txt".format(catalogue.strip(), date.strip(), title.strip())

def get_root_usage(tag):
    nouns = {"total":0, "k":0, "c":0, "e":0, "o": 0}
    verbs = {"total":0, "k":0, "c":0, "e":0, "o": 0}
    totals = {"total":0, "k":0, "c":0, "e":0, "o": 0}
    nr_chinese = 0
    nr_english = 0
    nr_korean = 0
    nr_jp = 0
    nr_unknown = 0
    ret = ""
    kr_eng_list = []
    kr_ch_list = []
    for t in tag["tags"]["tags"]:
        if t["class"] == 'Noun' or t["class"] == 'Verb':
            if t["type"] == "ko":
                nr_korean += 1
                totals["total"] += 1

                if t["class"] == 'Noun':
                    nouns["total"] += 1
                elif t["class"] == "Verb":
                    verbs["total"] += 1

                if "root" in t:
                    r = t["root"]
                    totals[r] += 1
                    if r == "e":
                        kr_eng_list.append(t["word"])
                    elif r == 'c':
                        kr_ch_list.append(t["word"])
                    if t["class"] == 'Noun':
                        nouns[r] += 1
                    elif t["class"] == "Verb":
                        verbs[r] += 1
            elif t["type"] == 'jp':
                nr_jp += 1
            elif t["type"] == 'zh':
                nr_chinese += 1
            elif t["type"] == 'en':
                nr_english += 1
            elif t["type"] == 'other':
                nr_unknown += 1
    ret += "Korean:{} Chinese:{} English:{} Japaness:{} Unknown:{}\n".format(nr_korean, nr_chinese, nr_english, nr_jp, nr_unknown)
    ret += "TotalKorean:{} k:{} c:{} e:{} o:{}\n".format(totals["total"], totals["k"], totals["c"], totals["e"], totals["o"])
    ret += "Nouns      :{} k:{} c:{} e:{} o:{}\n".format(nouns["total"], nouns["k"], nouns["c"], nouns["e"], nouns["o"])
    ret += "Verbs      :{} K:{} c:{} e:{} o:{}\n".format(verbs["total"], verbs["k"], verbs["c"], verbs["e"], verbs["o"])
    ret += "EnglishRoot:{}\n".format(kr_eng_list)
    ret += "ChineseRoot:{}\n".format(kr_ch_list)
    return ret



if __name__ == '__main__':
    usage="python mark_corpus.py corpus_path"
    # this command loads corpus_path/source.json, parse articles, and generate the output at corpus_path/ID.txt
    if len(sys.argv) >= 2:
        marker = MarkArticles(sys.argv[1])
        marker.parse_articles()
        marker.generate_tags()        
    else:
        print(usage)
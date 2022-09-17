import sys, os, json
from utils.word_root import parse_line

# Here is an example of the article in the corpus source.json.
# {"title",}
# {"title": "최려령 제12회 중국곡예 목단상 입선", "author": "", "catalogue": "문화일반-연변일보 Yanbian Daily", "date": "2022-05-27 09:07:02", "img": "http://www.iybrb.com/civ/images/2022
#-05/27/6d46760e-c434-42a8-b350-82450a623154.jpg", "summary": "일전 제12회 중국곡예 목단상 전국곡예시합 입선명단이 발표됐다.", "url": "http://www.iybrb.com/civ/content/2022-05/27/26_5535
#78.html", "content": "일전 제12회 중국곡예 목단상 전국곡예시합 입선명단이 발표됐다.길림성곡예가협회에서 추천한 2부의 작품과 길림성 2인전예술가협회에서 추천한 4부의 작품이 목단상에 입선
#됐는데 그중에는 량영우가 작사하고 강화가 감독, 최려령이 표현한 <오리정>이 들어있다.<오리정>은 춘향이 한양으로 떠나는 리몽룡과 오리정에서 리별하는 대목으로, 춘향의 리별을 앞둔 슬픈 심정
#을 생동하게 표현하는 작품이다. 일찍 2014년에 길림성곡예가협회의 지도하에 최려령은 제8회 중국곡예 목단상 ‘특별신인상’을 수상한 바 있다.입선된 6부의 작품은 길림성을 대표해 각 분회장의 시
#합에 참가하게 된다. 이것은 최근년에 길림성에서 입선 종목수가 가장 많은 한회이다. 중국곡예 목단상은 중국문련, 중국곡예가협회에서 공동 주최하는 전국성 곡예상으로 곡예 분야의 국가급 최고상
#이며 2년에 한번씩 개최한다.　　길림성곡예가협회에서는 온라인으로 곡예작품 세미나를 개최하고 관련 전문가에게 작품지도를 요청한 뒤 연습을 다그쳐 작품의 질을 높이고 좋은 성적을 따내 우리
#성의 영예를 빛낼 것이라 계획을 밝혔다. 중국길림넷"},

# source.json is an array of Yanbian articles
# source2root.json
# root.json
# 0.txt 1.txt 2.txt
# the count_tag.py translates the tag file to a tag object
# we should parse the source file and generates the both format, tag object in
# root.json and human readable plaintext file as 0.txt

class MarkArticles:
    def __init__(self):        
        self.articles = {}


    def load_articles_from_dir(self, corpus_path):
        self.articles_dirty = False        
        self.corpus_path = corpus_path
        self.corpus_source_file = corpus_path + '/source.json'
        self.tag_file = corpus_path = '/tag.json'
        #load source.json
        #load tag.json first
        # tag.json: {'url':{'source', source_object, 'tag': tag_object}}
        if os.path.exists(self.tag_file):
            with open(self.tag_file, 'r') as sf:
                self.articles = json.load(sf)
        if os.path.exists(self.corpus_source_file):
            with open(self.corpus_source_file) as sf:
                # an array of articles            
                for article in json.load(sf):
                    if 'url' not in article:
                        print("The URL is missing in article %s, skip it" % (article))
                        continue
                    url = article['url']
                    if url in self.articles:
                        print("The article %s is in tag.json already, skip it" % (url))
                    else:
                        print("Load article:%s" % (url))
                        self.articles[url] = {'source': article}
                        self.articles_dirty = True                                      
    def update_corpus_dir(self):
        if self.articles_dirty and self.tag_file:
            # update the tag_file
            with open(self.tag_file, 'w') as df:
                df.write(json.dumps(self.articles))
                self.articles_dirty = False

    # parse unparsed articles
    def parse_articles(self, all_articles = False):
        for k in self.articles:
            art = self.articles[k]
            if all_articles == True or 'tag' not in art:
                self.parse_article(art)
    
    def parse_article(self, art, update_article = True):
        root = {}
        source = art['source']     
        url = source["url"]
        title = source["title"]
        content = source["content"]
        tag_title = parse_line(title)
        tag_body = parse_line(content)
        if update_article:
            art['tag'] = {'title': tag_title, 'body':tag_body}        
        root_title = self.get_root_usage(tag_title)
        root_body = self.get_root_usage(tag_body)
        #merge tag_title_root_usage and tag_content_root_usage        

        for k in root_body:
            print('Merge key {}'.format(k))
            title_v = root_title[k]
            body_v = root_body[k]
            ak = "{}_{}".format('article',k)
            tk = "{}_{}".format('title', k)
            bk = "{}_{}".format('body', k)
            root[tk] = title_v
            root[bk] = body_v
            if k == 'tag_text':
                output = ""
                output += "url:{}\n".format(url)
                output += "=============================\n"
                output += title_v
                output += tag_title["view"]
                output += "=============================\n"
                output += body_v
                output += tag_body["view"]
                root[ak] = output
            else:
                root[ak] = title_v + body_v        
        return root



    def get_root_usage(self, tag):
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
        
        root = {}
        root['total_words'] = nr_chinese + nr_english + nr_korean + nr_jp + nr_unknown
        root['korean_words'] = nr_korean
        root['chinese_words'] = nr_chinese
        root['english_words'] = nr_english
        root['japanese_words'] = nr_jp
        root['kroot_words'] = totals['k']
        root['croot_words'] = totals['c']
        root['eroot_words'] = totals['e']
        root['oroot_words'] = totals['o']
        root['korean_noun'] = nouns['total']
        root['korean_kroot_noun'] = nouns['k']
        root['korean_croot_noun'] = nouns['c']
        root['korean_eroot_noun'] = nouns['e']
        root['korean_oroot_noun'] = nouns['o']
        root['korean_verb'] = nouns['total']
        root['korean_kroot_verb'] = verbs['k']
        root['korean_croot_verb'] = verbs['c']
        root['korean_eroot_verb'] = verbs['e']
        root['korean_oroot_verb'] = verbs['o']
        root['eroot_list'] = str(kr_eng_list)
        root['croot_list'] = str(kr_ch_list)
        root['tag_text'] = ret
        return root

#     def parse_article():

# def get_output_name(article):
#     catalogue = article["catalogue"]
#     if type(catalogue) == list:
#         catalogue = catalogue[-2]
#     if catalogue == "":
#         catalogue = "unknown"
#     title = article["title"]
#     date = article["date"]
#     return "{}-{}-{}.txt".format(catalogue.strip(), date.strip(), title.strip())




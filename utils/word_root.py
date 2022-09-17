import sys
from konlpy.tag import Okt
import json
import os
from utils.utils import char_type_detect
from utils.naverDict import NaverDict
import unicodedata

def extract_article(source, index):
    articles = json.load(open(source,'r'))
    for a in articles:
        if index == a['url']:
            return a
    return None


def split_lines(p, line_length=50):
    words = p.split()
    ret = ""
    line = 0
    for w in words:
        ret += w
        line += terminal_length(w)
        if line > line_length:
            ret += '\n'
            line = 0
        else:
            ret += ' '
    return ret


def terminal_length(str):
    width = 0.0
    for c in str:
        if (unicodedata.east_asian_width(c) == 'W'):
            if char_type_detect(c) == 'ko':
                width += 1.5
            else:
                width += 2
        else:
            width += 1
    return width

# The input is a Korean basestrin
# //Output:
# // { "raw": p,
# //   "tags": [{"word": w, "type":w_type, "pos": pos, "class": c, "root": ""}]
# //   "view": [{'line':{}, 'marker':{}}]
# // }

def reconstruct_line(tl):
    tags = tl["tags"]
    ret = ""
    for t in tags:
        ret += "{}{}".format(t["prefix"], t["word"])
    return ret

def mark_line(tl, line_length = 90):
    cur = 0
    tags = tl["tags"]
    curr_line = ""
    curr_mark = ""
    l_cursor = 0.0
    m_cursor = 0.0
    ret = ""
    for t in tags:
        view = view_tag(t, l_cursor, m_cursor)
        curr_line += view[0]["view"]
        l_cursor = view[0]["cursor"]
        curr_mark += view[1]["view"]
        m_cursor = view[1]["cursor"]
        if m_cursor > line_length:
            ret += curr_line + "\n"
            ret += curr_mark + "\n"
            curr_line = ""
            curr_mark = ""
            l_cursor = 0.0
            m_cursor = 0.0
    if curr_mark != "":
        ret += curr_line + "\n"
        ret += curr_mark + "\n"
    return ret

def tag_line(l, verbose = False):
    #lp = split_lines(p)
    ret = { "raw": l,
            "tags": [],
            "view": []
            }
    kd = NaverDict()
    raw_str = ret["raw"]
    tags = Okt().pos(raw_str)
    curr = 0
    ret_tags = ret["tags"]
    # for each tag, search the first time that the tag appears in the raw string
    for t in tags:
        # tag format (word, class)
        w = t[0]
        c = t[1]
        w_type = char_type_detect(w)
        pos = []
        start = raw_str[curr:].find(w)
        if start != -1:
            prefix = raw_str[curr:curr+start]
            pos_start = curr + len(prefix)
            pos_end = curr+len(prefix) + len(w)
            pos = [pos_start, pos_end]
            curr = pos_end
            tag = {"word": w, "prefix": prefix, "type": w_type, "class": c, "root": "o", "pos": pos}
            if (tag["class"] == 'Noun' or tag["class"] == 'Verb') and tag["type"] == "ko":
                # now lets search this word
                try:
                    naver = kd.search(w)
                    if naver and len(naver) > 0:
                        tag["naver"] = naver
                        first_exp = naver[0]
                        if "root" in first_exp:
                            root_type = first_exp["root"][1]
                            print("Found root:{} for word:{}".format(first_exp["root"], w)) if verbose else 0
                            if root_type == "en":
                                tag["root"] = 'e'
                            elif root_type == "zh":
                                tag["root"] = 'c'
                            else:
                                tag["root"] = 'k'
                        else:
                            tag["root"] = 'k'
                except Exception as e:
                    print("Exception:{} while searching word {}".format(e, w)) if verbose else 0
            ret_tags.append(tag)
        else:
            sys.stderr.write("Failed to find tag {}".format(tag))
    kd.update()
    return ret

def get_width(w, l_cursor, m_cursor):
    if l_cursor > m_cursor or m_cursor - l_cursor > 1:
        print('WARN: l_cursor is a head of m_cursor:{} {}'.format(l_cursor, m_cursor))
    #print("Analyze {} {} {}".format(w, l_cursor, m_cursor))
    l_width = terminal_length(w)
    if l_width == 0:
        return [0, 0]
    gap = m_cursor - l_cursor
    m_width = l_width - gap
    if not m_width.is_integer():
        m_width = int(m_width) + 1
    return [l_width, int(m_width)]


# return ["t["prefix"]t["word"]", ".....c....."]
def view_tag(t, l_cursor, m_cursor):

    gap = m_cursor - l_cursor
    words = [t["prefix"], t["word"]]
    l = ""
    m = ""
    prefix = t["prefix"]
    word = t["word"]

    widths = get_width(prefix, l_cursor, m_cursor)
    l += '{}'.format(prefix)
    l_cursor += widths[0]
    m += '.'*widths[1]
    m_cursor += widths[1]

    widths = get_width(word, l_cursor, m_cursor)
    l += '{}'.format(word)
    l_cursor += widths[0]
    marker = '.'
    if (t["class"] == 'Noun' or t["class"] == 'Verb') and t["type"] == "ko":
        marker = t["root"]
    m += "{}{}".format(marker, '.'*(widths[1]-1))
    m_cursor += widths[1]
    return [{"view":l,"cursor":l_cursor}, {"view":m,"cursor":m_cursor}]

def parse_line(content):
    content_tags = tag_line(content)
    rec_content = reconstruct_line(content_tags)
    view = mark_line(content_tags)
    return {"tags": content_tags, "view": view}


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
def mark_article(source):
    root = {}    
    url = source['url']
    title = source["title"]
    content = source["content"]
    tag_title = parse_line(title)
    tag_body = parse_line(content)
    root_title = get_root_usage(tag_title)
    root_body = get_root_usage(tag_body)
    #merge tag_title_root_usage and tag_content_root_usage        
    for k in root_body:        
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


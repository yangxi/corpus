import sys
from konlpy.tag import Okt
import json
import os
from utils import char_type_detect
from naverDict import NaverDict
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

def tag_line(l):
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
                            print("Found root:{} for word:{}".format(first_exp["root"], w))
                            if root_type == "en":
                                tag["root"] = 'e'
                            elif root_type == "zh":
                                tag["root"] = 'c'
                            else:
                                tag["root"] = 'k'
                        else:
                            tag["root"] = 'k'
                except Exception as e:
                    print("Exception:{} while searching word {}".format(e, w))
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


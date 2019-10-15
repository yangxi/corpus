# url:http://www.iybrb.com/civ/content/2014-01/09/26_51753.html
# =============================
# Korean:6 Chinese:0 English:0 Japaness:0 Unknown:0
# TotalKorean:6 k:1 c:5 e:0 o:0
# Nouns      :6 k:1 c:5 e:0 o:0
# Verbs      :0 K:0 c:0 e:0 o:0
# EnglishRoot:[]
# ChineseRoot:['연길', '명절', '하향', '공연', '개시']
# 연길 명절맞이 문예하향공연 개시
# c...c..k......c..c...c..
# =============================
# Korean:138 Chinese:0 English:0 Japaness:0 Unknown:0
# TotalKorean:138 k:45 c:88 e:1 o:4
# Nouns      :114 k:23 c:86 e:1 o:4
# Verbs      :24 K:22 c:2 e:0 o:0
# EnglishRoot:['몽골']
# ChineseRoot:['공연', '주한', '촬영', '음력설', '정월', '대보름', '연길시', '화관', '명절', '하향', '공연', '조직', '오전', '연길시', '공연', '오전', '명절', '분위기', '흥', '흥', '연길시', '연길시', '화관', '연길시', '조선족', '예술', '단', '연길시', '예술', '단', '연길시', '화관', '관악단', '의', '여명', '무용', '소품', '등', '공연', '촌민', '명절', '축복', '전', '소품', '나도', '소품', '부자', '등', '농촌', '실정', '창작', '작품', '촌민', '공감', '공연', '고조', '산동', '동북', '결합', '무용', '환락', '창작', '조선족', '정', '담아', '등', '박수갈채', '연길시', '화관', '백', '남부', '관장', '명절', '하향', '공연', '선후', '천진', '삼도', '무장', '연변', '변', '방지', '연변', '영원', '등지', '차', '국화', '기자']

# Given a txt file formatted with the above pattern, generate output:
import sys


def extract_url(partone):
    ret = ""
    t = partone.split("\n")
    if t[0].startswith('url'):
        ret = t[0][4:]
    return ret
def extract_word_count(parttwo):
    ret = {}
    for l in parttwo.split('\n'):
        if l.startswith("TotalKorean"):
            t = l.split(' ')
            for kv in t:
                kvc = kv.split(':')
                ret[kvc[0]] = kvc[1]
    return ret
def extract_title(partone):
    l = partone.split('\n')
    return l[-3]
def extract_array(part, key):
    ret = []
    for l in part.split('\n'):
        if l.startswith(key):
            kv = l.split(':')
            ret = eval(kv[1])
    return ret

def report_csv(parsed):
    #url | title | TotalKorean | k | c | e | o | englishroot | chineseroot
    url = parsed["url"]
    title = parsed["title"]
    t_korean = parsed["korean_root_count"]["TotalKorean"]
    r_korean = parsed["korean_root_count"]["k"]
    r_chinese = parsed["korean_root_count"]["c"]
    r_english = parsed["korean_root_count"]["e"]
    r_other = parsed["korean_root_count"]["o"]
    e_list = parsed["english_root"]
    c_list = parsed["chinese_root"]
    ret = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(url, title, t_korean, r_english, r_chinese, r_korean, r_other,e_list, c_list)
    return ret;


def parse_yanbian_mark(output):
    parsed_mark = {}
    parts = output.split("=============================")
    parsed_mark["url"] = extract_url(parts[0])
    parsed_mark["title"] = extract_title(parts[1])
    parsed_mark["korean_root_count"] = extract_word_count(parts[2])
    parsed_mark["english_root"] = extract_array(parts[2], 'EnglishRoot')
    parsed_mark["chinese_root"] = extract_array(parts[2], 'ChineseRoot')
    return parsed_mark

if __name__ == '__main__':
    usage="python count_tag.py parsed_word_count.txt"
    if len(sys.argv) < 2:
        print(usage)
        exit(1)
    else:
        print("url\ttitle\tTotalKorean\tEnglishRoot\tChineseRoot\tKoreanRoot\tUnknownRoot\tEnglishRootList\tChineseRootList")
        for i in sys.argv[1:]:
            with open(i, 'r') as f:
                output = f.read()
                parsed = parse_yanbian_mark(output)
                print(report_csv(parsed))


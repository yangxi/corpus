import sys, os

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

# ret{}
#  url: str
#  title: str
#  prefix: title|body|article_tag
#
#   PREFIX_total_words: integer
#   PREFIX_korean_words: integer
#   PREFIX_chinese_words: integer
#   PREFIX_english_words:
#   PREFIX_japaness_words:
#   PREFIX_unknown_words:

#   PREFIX_kroot_words:
#   PREFIX_croot_words:
#   PREFIX_eroot_words:
#   PREFIX_oroot_words:
#   
#   PREFIX_korean_noun:
#   PREFIX_korean_kroot_noun:
#   PREFIX_korean_croot_noun:
#   PREFIX_korean_eroot_noun:
#   PREFIX_korean_oroot_noun:
#
#   PREFIX_korean_verb:
#   PREFIX_korean_kroot_verb:
#   PREFIX_korean_croot_verb:
#   PREFIX_korean_eroot_verb:
#   PREFIX_korean_oroot_verb:
#
#   PREFIX_eroot_list:
#   PREFIX_croot_list:

#   PREFIX_tag_text:


class TaggedArticle:

    def __init__(self, tagfile):
        self.tag = {}
        self.tag_source_path = ""
        self.parsing_error = ""
        
        fpath = tagfile
        if tagfile.startswith("~"):
            fpath = os.path.expanduser(fpath)                   
        if os.path.exists(fpath):
            self.tag_source_path = fpath
            self.parse_tags()
        else:
            self.parsing_error += "The tag file %s does not exist.\n" % (fpath)
            raise Exception(self.parsing_error)
    
    def parse_tags(self):
        with open(self.tag_source_path, 'r') as tagf:            
            parts = tagf.read().split("=============================")
            if len(parts) != 3:
                self.parsing_error += "The tag file does not have three parts.\n"                
                raise Exception(self.parsing_error)
            url_part = parts[0].strip('\n')
            title_part = parts[1].strip('\n')
            body_part = parts[2].strip('\n')
            self.extract_url(url_part)
            self.extract_part("title", title_part)
            self.extract_part("body", body_part)
            self.compute_article()
            article_title = self.tag['title_tag_text'].split('\n')[0]
            self.tag['title'] = article_title
            self.tag['tag_file_path'] = self.tag_source_path
            

    def compute_article(self):
        for k in list(self.tag.keys()):
            if k.startswith('title'):
                paired_key = k.replace('title', 'body')
                if paired_key in self.tag:
                    article_key = k.replace('title', 'article')
                    article_value = self.tag[k] + self.tag[paired_key]
                    self.tag[article_key] = article_value
    def extract_url(self, url_part):
        if url_part.startswith('url:'):
            self.tag['url'] = url_part[4:]
        else:
            self.parsing_error += "The url is missing.\n"
            raise Exception(self.parsing_error)
    
    def extract_part(self, prefix, part):
        lines = part.split('\n')
        if len(lines) < 6:
            self.parsing_error += "The {} part has less than 6 lines\n".format(prefix, part)
            raise Exception(self.parsing_error)
        total_word_root_line = lines[0]
#        print(part)
#        print("The first line %s" % (str(lines)))
        self.parse_total_word_line(prefix, total_word_root_line)
        korean_word_root_line = lines[1]
        self.parse_korean_word_root_line(prefix, korean_word_root_line)
        korean_noun_root_line = lines[2]
        self.parse_korean_nounverb_root_line(prefix, korean_noun_root_line, 'Nouns', 'nouns')
        korean_verb_root_line = lines[3]
        self.parse_korean_nounverb_root_line(prefix, korean_verb_root_line, 'Verbs', 'verbs')
        english_root_list = lines[4]
        chinese_root_list = lines[5]
        self.parse_root_list(prefix, [english_root_list, chinese_root_list])
        # PREFIX_tag_text
        if len(lines) == 6:
            #empty content
            tag_text = ""
        else:        
            tag_text = "\n".join(lines[6:])
        tag_key = "{}_tag_text".format(prefix)
        self.tag[tag_key] = tag_text
        
    
    def kv_from_line(self, line, key_map, trans_v = lambda x: int(x)):
        ret = {}
        if line.startswith('Nouns      :'):
            line = line.replace('Nouns      :', 'Nouns:')
        if line.startswith('Verbs      :'):
            line = line.replace('Verbs      :', 'Verbs:')
        if line.startswith('EnglishRoot:'):
            t = [line]
        elif line.startswith('ChineseRoot:'):
            t = [line]
        else:
            t = line.split(' ')
        for kv in t:
            kvc = kv.split(':')
            if len(kvc) != 2:
                self.parsing_error += "Failed to extract kv from the item {} in line {}.\n".format(kv, line)
                raise Exception(self.parsing_error)
            new_k = kvc[0].strip()
            new_v = trans_v(kvc[1])
            if new_k in key_map:
                new_k = key_map[new_k]
                ret[new_k] = new_v
        return ret
    #   PREFIX_eroot_list:
    #   PREFIX_croot_list:

    def parse_root_list(self, prefix, lines):
        kmap = {'EnglishRoot': "{}_eroot_list".format(prefix), 'ChineseRoot': "{}_croot_list".format(prefix)}
        for l in lines:        
            kv = self.kv_from_line(l, kmap, lambda x: x)
            if len(list(kv.keys())) != 1:
                self.parsing_error += "The Root list is missing from the line {}\n".format(l)
                raise Exception(self.parsing_error)
            for k in kv:
                self.tag[k] = kv[k]

    # prefix: title_tag | body_tag 
    # Korean:6 Chinese:0 English:0 Japaness:0 Unknown:0
    #   PREFIX_total_words: integer
    #   PREFIX_korean_words: integer
    #   PREFIX_chinese_words: integer
    #   PREFIX_english_words:
    #   PREFIX_japaness_words:
    #   PREFIX_unknown_words:
    def parse_total_word_line(self, prefix, word_line):
            kmap = {"Korean":"{}_korean_words".format(prefix), "Chinese":"{}_chinese_words".format(prefix), "Japaness":"{}_japaness_words".format(prefix),"Unknown":"{}_unknow_words".format(prefix)}
            kv = self.kv_from_line(word_line, kmap)            
            nr_key = len(list(kv.keys()))
            if (nr_key != 4):
                self.parsing_error += "The {} line does not have 4 parts: {}\n".format(prefix, word_line)
            for k in kv:
                self.tag[k] = kv[k]
            total_count = sum(kv.values())
            total_key = "{}_total_words".format(prefix)
            self.tag[total_key] = total_count            

    # TotalKorean:103 k:16 c:78 e:3 o:6
    #   PREFIX_kroot_words:
    #   PREFIX_croot_words:
    #   PREFIX_eroot_words:
    #   PREFIX_oroot_words:
    def parse_korean_word_root_line(self, prefix, korean_root_line):
            kmap = {"k":"{}_kroot_words".format(prefix), "K":"{}_kroot_words".format(prefix),"c":"{}_croot_words".format(prefix),"e":"{}_oeoot_words".format(prefix),"o":"{}_oroot_words".format(prefix)}
            kv = self.kv_from_line(korean_root_line, kmap)            
            nr_key = len(list(kv.keys()))
            if (nr_key != 4):
                self.parsing_error += "The {} line does not have 4 parts: {}\n".format(prefix, korean_root_line)
                raise Exception(self.parsing_error)
            for k in kv:
                self.tag[k] = kv[k]       
    # Nouns      :90 k:5 c:77 e:3 o:5
    #   PREFIX_korean_noun:
    #   PREFIX_kroot_noun:
    #   PREFIX_croot_noun:
    #   PREFIX_eroot_noun:
    #   PREFIX_oroot_noun:
    def parse_korean_nounverb_root_line(self, prefix, root_line, source_type, target_type):
            kmap = {source_type:"{}_korean_{}".format(prefix, target_type), "k":"{}_kroot_{}".format(prefix, target_type), "K":"{}_kroot_{}".format(prefix, target_type), "c":"{}_croot_{}".format(prefix, target_type),  "e":"{}_eroot_{}".format(prefix, target_type),  "o":"{}_oroot_{}".format(prefix, target_type)}
            kv = self.kv_from_line(root_line, kmap)            
            nr_key = len(list(kv.keys()))
            if (nr_key != 5):
                self.parsing_error += "The {} line does not have 5 parts: {}\n".format(prefix, root_line)
                raise Exception(self.parsing_error)
            for k in kv:
                self.tag[k] = kv[k]    
    
# # Korean:6 Chinese:0 English:0 Japaness:0 Unknown:0
# # TotalKorean:6 k:1 c:5 e:0 o:0
# # Nouns      :5 k:0 c:5 e:0 o:0
# # Verbs      :1 K:1 c:0 e:0 o:0
# # EnglishRoot:[]
# # ChineseRoot:['전국', '소수민족', '탁구', '경기', '연변']
# # 2010년 전국 소수민족탁구경기 연변서 펼친다
#     def parse_title(self, title_part):
        
# def parse_wordroot_text(output):
#     parsed_mark = {}
#     parts = output.split("=============================")
#     parsed_mark["url"] = extract_url(parts[0])
#     parsed_mark["title"] = extract_title(parts[1])
#     parsed_mark["korean_root_count"] = extract_word_count(parts[2])
#     parsed_mark["english_root"] = extract_array(parts[2], 'EnglishRoot')
#     parsed_mark["chinese_root"] = extract_array(parts[2], 'ChineseRoot')
#     return parsed_mark

# def extract_url(partone):
#     ret = ""
#     t = partone.split("\n")
#     if t[0].startswith('url'):
#         ret = t[0][4:]
#     return ret

# #  title_nouns_total_kword: integer
# #  title_nouns_total_kroot:
# #  title_nouns_total_croot:
# #  title_nouns_total_eroot:
# #  title_nouns_total_oroot:
# def extract_kword_count(body, line_prefix, output_key_prefix, output):
#     ret = {}
#     for l in body.split('\n'):
#         if l.startswith(line_prefix):
#             t = l.split(' ')
#             for kv in t:
#                 kvc = kv.split(':')
#                 ret[kvc[0]] = int(kvc[1])
#     return ret

# def extract_title(partone):
#     l = partone.split('\n')
#     return l[-3]
# def extract_array(part, key):
#     ret = []
#     for l in part.split('\n'):
#         if l.startswith(key):
#             kv = l.split(':')
#             ret = eval(kv[1])
#     return ret

# # The body is the lines followed by the line starting with the key
# def extract_array(part, key="ChineseRoot"):    
#     lines = part.split('\n')
#     for i in range(0, len(lines)):
#         if lines[i].startswith(key):
#             return lines[i+1]

# def report_csv(parsed):
#     #url | title | TotalKorean | k | c | e | o | englishroot | chineseroot
#     url = parsed["url"]
#     title = parsed["title"]
#     t_korean = parsed["korean_root_count"]["TotalKorean"]
#     r_korean = parsed["korean_root_count"]["k"]
#     r_chinese = parsed["korean_root_count"]["c"]
#     r_english = parsed["korean_root_count"]["e"]
#     r_other = parsed["korean_root_count"]["o"]
#     e_list = parsed["english_root"]
#     c_list = parsed["chinese_root"]
#     ret = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(url, title, t_korean, r_english, r_chinese, r_korean, r_other,e_list, c_list)
#     return ret;

# if __name__ == '__main__':
#     usage="python count_tag.py parsed_word_count.txt"
#     if len(sys.argv) < 2:
#         print(usage)
#         exit(1)
#     else:
#         print("url\ttitle\tTotalKorean\tEnglishRoot\tChineseRoot\tKoreanRoot\tUnknownRoot\tEnglishRootList\tChineseRootList")
#         for i in sys.argv[1:]:
#             with open(i, 'r') as f:
#                 output = f.read()
#                 parsed = parse_yanbian_mark(output)
#                 print(report_csv(parsed))


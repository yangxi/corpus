import sys
from word_root import parse_line
from yanbiandaily import YanbianDaily

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
    return ret

def parse_article(url, outputfile=None):
    yanbian = YanbianDaily()
    article = yanbian.search_page(url)
    yanbian.update_pages()
    title = article["title"]
    content = article["content"]
    tag_title = parse_line(title)
    tag_content = parse_line(content)
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

    print(output)
    with open(outputfile,'w') as outf:
        print("Write the view to file:{}".format(outputfile))
        outf.write(output)

if __name__ == '__main__':
    usage="python word_root.py url [target_file]"
    if len(sys.argv) >= 3:
        parse_article(sys.argv[1], sys.argv[2])
    elif len(sys.argv) >= 2:
        parse_article(sys.argv[1])
    else:
        print(usage)
import sys
from word_root import parse_line
from yanbiandaily import YanbianDaily

def parse_article(url):
    yanbian = YanbianDaily()
    article = yanbian.search_page(url)
    yanbian.update_pages()
    title = article["title"]
    content = article["content"]
    tag_title = parse_line(title)
    content = article["content"]
    tag_content = parse_line(content)
    print(tag_title["view"])
    print(tag_content["view"])

if __name__ == '__main__':
    usage="word_root.py url"
    parse_article(sys.argv[1])
import scrapy

# title

#<title>경제일반-연변일보 Yanbian Daily</title>

# # articles
# ```<!--列表内容-->
#
# 	<div class="news_list">
# 		<div class="thumb_con">
# 			<div class="a"><a href="http://www.iybrb.com/eco/content/2019-01/03/7_339575.html" target="_blank"><img src="http://www.iybrb.com/eco/images/2019-01/03/28baeb55-3853-4da5-8747-f6d6aa5496f3.jpg" width="200px" height="110px" /></a></div>
# 			<div class="b">
# 				<p class="title"><a href="http://www.iybrb.com/eco/content/2019-01/03/7_339575.html" target="_blank">마천자향, 빈곤해탈 난관공략 사업 지속화</a></p>
# 				<p class="at"><span class="author">최은정 기자</span> <span class="pubTime">2019-01-03 09:09:59</span></p>
# 				<p class="summary"><a href="http://www.iybrb.com/eco/content/2019-01/03/7_339575.html" target="_blank">나머지 9세대 빈곤해탈 담보
# 올해 훈춘시 마천자향에서는 지속적으로 빈곤해탈 난관공략 사업으로 경제, 사회 발전을 도모하고 향촌진흥 전략과 결합해 경제의 안정적이면서 건전한 발전을 추진함으로써 사회의 조화로운 안정을 추동하게 된다.</a></p>
# 			</div>
# 			<div class="sep"></div>
# 		</div>
#
#
# 		<div class="thumb_con">
# 			<div class="a"><a href="http://www.iybrb.com/eco/content/2019-01/03/7_339571.html" target="_blank"><img src="http://www.iybrb.com/eco/images/2019-01/03/730abe91-d0dc-4304-8dd4-93af802ea422.jpg" width="200px" height="110px" /></a></div>
# 			<div class="b">
# 				<p class="title"><a href="http://www.iybrb.com/eco/content/2019-01/03/7_339571.html" target="_blank">소형 기업 위한 세수우대정책 출범</a></p>
# 				<p class="at"><span class="author">최은정 기자</span> <span class="pubTime">2019-01-03 09:04:39</span></p>
# 				<p class="summary"><a href="http://www.iybrb.com/eco/content/2019-01/03/7_339571.html" target="_blank">기업소득세 감면 등 혜택 망라
# 주국가세무국에 따르면 일전 소형 기업 및 개체공상호들을 대상으로 한 세수우대정책이 출범되여 납세자들에게 세수우대 혜택이 차례지게 된다.</a></p>
# 			</div>
# 			<div class="sep"></div>
# 		</div>
# ```

class YanbianSpider(scrapy.Spider):
    # url: {"type":"index"|"article", "status":"start"|"done", "payload":{"title", "catalogue", "date", "author", "img", "content"}}
    name = 'yanbian'
    nr_page = 2;
    init_pages = [
        'http://www.iybrb.com/eco/7.html',
        'http://www.iybrb.com/eco/9.html',
        'http://www.iybrb.com/eco/10.html',
        'http://www.iybrb.com/eco/63.html',
        'http://www.iybrb.com/eco/11.html',
        'http://www.iybrb.com/eco/12.html',
        'http://www.iybrb.com/eco/13.html',
        'http://www.iybrb.com/eco/14.html',
        'http://www.iybrb.com/soc/19.html',
        'http://www.iybrb.com/soc/21.html',
        'http://www.iybrb.com/soc/22.html',
        'http://www.iybrb.com/soc/24.html',
        'http://www.iybrb.com/soc/25.html',
        'http://www.iybrb.com/civ/26.html',
        'http://www.iybrb.com/civ/26.html',
        'http://www.iybrb.com/civ/27.html',
        'http://www.iybrb.com/civ/28.html',
        'http://www.iybrb.com/civ/29.html',
        'http://www.iybrb.com/civ/30.html',
        'http://www.iybrb.com/civ/31.html',
        'http://www.iybrb.com/news/59.html',
        'http://www.iybrb.com/news/60.html',
        'http://www.iybrb.com/news/61.html',
        'http://www.iybrb.com/news/62.html',
        'http://www.iybrb.com/com/54.html',
        'http://www.iybrb.com/com/55.html',
        'http://www.iybrb.com/com/56.html',
        'http://www.iybrb.com/pol/15.html',
        'http://www.iybrb.com/pol/16.html',
        'http://www.iybrb.com/pol/17.html',
        'http://www.iybrb.com/pol/18.html',
        'http://www.iybrb.com/env/40.html',
        'http://www.iybrb.com/env/41.html',
        'http://www.iybrb.com/env/42.html',
        'http://www.iybrb.com/env/66.html',
        'http://www.iybrb.com/env/355.html',
        'http://www.iybrb.com/pla/46.html',
        'http://www.iybrb.com/pla/46.html',
        'http://www.iybrb.com/pla/47.html',
        'http://www.iybrb.com/pla/48.html',
        'http://www.iybrb.com/pla/65.html',
        'http://www.iybrb.com/ser/50.html',
        'http://www.iybrb.com/ser/51.html'    
        'http://www.iybrb.com/sport/34.html',
        'http://www.iybrb.com/sport/35.html',
        'http://www.iybrb.com/sport/36.html',
        'http://www.iybrb.com/sport/37.html',
        'http://www.iybrb.com/sport/38.html'
    ];
    #        'http://www.iybrb.com/pol/15.html': {"type": "index", "status": "start", "payload": {}},
    #        'http://www.iybrb.com/eco/7.html': {"type": "index", "status": "start", "payload": {}},
    pages = {
    };
    def start_requests(self):
        index_url  = getattr(self, 'index', None);
        nr_index_page = getattr(self, 'page', None);
        if nr_index_page is not None:
            self.nr_page = int(nr_index_page);
        starting_urls = [];
        if index_url is not None:
            print("Using paseed index page " + index_url);
            url = index_url;
            if url not in self.pages:
                self.pages[url] = {"type":"index", "status":"start", "payload":{}};
            starting_urls.append(url);
        else:
            starting_urls = self.init_pages;
        for url in starting_urls:
            self.pages[url] = {"type":"index", "init": True, "status":"start", "payload":{}}
            yield scrapy.Request(url, self.parse);

    def extract_string(self, extract, default=""):
        if len(extract) == 1:
            return extract[0];
        return default;

    def parse(self, response):
        url = response._url;
        if not url in self.pages:
            print("Unknown URL:" + url);
            yield;
        url_status = self.pages[url];
        if (url_status['status'] is not "start"):
            print("We have processed or are processing URL " + url);
            yield;
        # start to process this page
        url_status['status'] = 'going';
        print("Processing index page " + url);
        print(url_status);
        if (url_status['type'] == 'index'):
            # Done this page
            # fill title
            catalogue = response.css('title::text').extract()[0];
            url_status['catalogue'] = catalogue;
            # process all articles in this index page
            articles = response.css('div.news_list').css('div.thumb_con');
            for article in articles:
                article_url = self.extract_string(article.css('div.thumb_con').css('div.b').css('p.title').css('a::attr(href)').extract());
                print("Processing item " + article_url);
                if article_url not in self.pages:
                    article_img = self.extract_string(article.css('div.thumb_con').css('div.a').css('img::attr(src)').extract());
                    article_title = self.extract_string(article.css('div.thumb_con').css('div.b').css('p.title').css('a::text').extract());
                    article_author = self.extract_string(article.css('div.thumb_con').css('div.b').css('p.at').css('span.author::text').extract());
                    article_date = self.extract_string(article.css('div.thumb_con').css('div.b').css('p.at').css('span.pubTime::text').extract());
                    article_summary = self.extract_string(article.css('div.thumb_con').css('div.b').css('p.summary').css('a::text').extract());
                    article_dict = {"type": "article", "status": "start", "payload": {"title": article_title, "author": article_author, "catalogue": catalogue, "date": article_date,
                                 "img": article_img, "summary": article_summary, "url": article_url}};
                    self.pages[article_url] = article_dict;
                    # yield article_dict;
                    # follow the article link
                    yield scrapy.Request(article_url, callback=self.parse);

            # next index pages
            if (url_status["init"] == True):
                for i in range(2, self.nr_page + 1):
                    next_page = response.css('li.page' + str(i));
                    if len(next_page) == 0:
                        print("Index page " + url + " does not have page " + str(i));
                    else:
                        next_page_url = self.extract_string(next_page.css('a::attr(href)').extract());
                        if (next_page_url is not "" and next_page_url.startswith("http://www.iybrb.com")):
                            if (next_page_url not in self.pages):
                                self.pages[next_page_url] = {"type":"index", "init": False, "status":"start", "payload":{}};
                                print("Add one index page, url: " + str(next_page_url));
                                yield scrapy.Request(next_page_url, callback=self.parse);
            url_status['status'] = 'done';

        elif (url_status['type'] == 'article'):
            print("Processing article " + url);
            # extract the content;
            article_dict = url_status["payload"];
            article_content = response.css('div.content').css('p::text');
            article_str = "";
            if (len(article_content) == 0):
                print("Empty content");
            for p in article_content:
                article_str += p.extract();
            article_dict["content"] = article_str;
            url_status['status'] = 'done';
            yield article_dict;
        else:
            print("Unknown type of page " + url);

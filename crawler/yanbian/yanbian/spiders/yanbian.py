import scrapy
import json

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
    name = 'yanbian'

    init_pages = []
    def __init__(self, task=None, *args, **kwargs):
        super(YanbianSpider, self).__init__(*args, **kwargs)
        if task:
            if task.endswith('.json'):
                # [{"url":"http://xxx", "start_page":number, "end_page":number}...]
                with open(task, 'r') as f:
                    self.init_pages = json.load(f)
            else:
                with open(task, 'r') as f:
                    pages = f.readlines()
                    for l in pages:
                        t = l.split(' ')
                        p_url = t[0]
                        if not p_url.startswith("http://"):
                            printf("Task file is not in right format, wrong url:{}".format(p_url))
                            exit(1)
                        s_p = int(t[1])
                        e_p = int(t[2])
                        if e_p < s_p:
                            printf("task file is not in right format, end_page is smaller than start_page: {} < {}".format(e_p,s_p))
                            exit(1)
                        self.init_pages.append({"url":p_url, "start_page":s_p, "end_page":e_p})
        else:
            printf("scrapy crawl yanbian -o task=./INITPAGE.json")
            exit(1)

    pages = {
    };
    def start_requests(self):
        index_url  = getattr(self, 'index', None);
        nr_index_page = getattr(self, 'page', None);
        starting_urls = [];
        if index_url is not None:
            print("Using paseed index page " + index_url);
            url = index_url;
            if url not in self.pages:
                self.pages[url] = {"type":"index", "status":"start", "payload":{}};
            starting_urls.append(url);
        else:
            starting_urls = self.init_pages;
        for url_request in starting_urls:
            url = url_request["url"];
            start_page = url_request["start_page"];
            end_page = url_request["end_page"];
            self.pages[url] = {"type":"index", "init": True, "status":"start", "payload":{"start_page":start_page, "current_page":start_page, "end_page":end_page}}
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
            # <div class="news_list"> 
	    #     <div class="thumb_con">
	    #     	<div class="a"><a href="http://www.iybrb.com/eco/content/2019-05/13/12_356173.html" target="_blank"><img src="http://www.iybrb.com/eco/images/2019-05/13/1060c839-8727-4412-b877-f91e307aca98.jpg" width="200px" height="110px" /></a></div>
	    #     	<div class="b">
	    #     		<p class="title"><a href="http://www.iybrb.com/eco/content/2019-05/13/12_356173.html" target="_blank">울긋불긋 봄의 선물, 튤립축제 비암산문화관광풍경구에서 개막</a></p>
	    #     		<p class="at"><span class="author">리현준,심연 기자</span> <span class="pubTime">2019-05-13 09:31:15</span></p>
	    #     		<p class="summary"><a href="http://www.iybrb.com/eco/content/2019-05/13/12_356173.html" target="_blank">5월을 맞아 봄빛이 완연한 룡정시 비암산문화관광풍경구에서 12일, ‘첫회 네델란드 튤립(郁金香)축제’가 개막했다.</a></p>
	    #     	</div>
	    #     	<div class="sep"></div>
	    #     </div>
 

            articles = response.css('div.news_list').css('div.thumb_con');            
            for article in articles:
                article_url = self.extract_string(article.css('div.thumb_con').css('div.b').css('p.title').css('a::attr(href)').extract());
                print("Processing item in thumb_con format " + article_url);
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
            # <div class="news_list"> 
	    #     <div class="txt_con">
	    #     	<p class="title"><a href="http://www.iybrb.com/eco/content/2009-02/17/12_25032.html" target="_blank">주공상계통 금융위기대처조치 출범</a></p>
	    #     	<p class="at"><span class="author"></span> <span class="pubTime">2009-02-17 18:25:11</span></p>
	    #     	<p class="summary"><a href="http://www.iybrb.com/eco/content/2009-02/17/12_25032.html" target="_blank"></a></p>
	    #     	<div class="sep"></div>
	    #     </div>
            articles = response.css('div.news_list').css('div.txt_con');
            # next index pages
            for article in articles:
                article_url = self.extract_string(article.css('div.txt_con').css('p.title').css('a::attr(href)').extract());
                if article_url not in self.pages:
#                    article_img = self.extract_string(article.css('div.thumb_con').css('div.a').css('img::attr(src)').extract());
                    article_title = self.extract_string(article.css('div.txt_con').css('p.title').css('a::text').extract());
                    article_author = self.extract_string(article.css('div.txt_con').css('p.at').css('span.author::text').extract());
                    article_date = self.extract_string(article.css('div.txt_con').css('p.at').css('span.pubTime::text').extract());
                    article_summary = self.extract_string(article.css('div.thumb_con').css('p.summary').css('a::text').extract());
                    article_dict = {"type": "article", "status": "start", "payload": {"title": article_title, "author": article_author, "catalogue": catalogue, "date": article_date,
                                 "summary": article_summary, "url": article_url}};
                    self.pages[article_url] = article_dict;
                    # yield article_dict;
                    # follow the article link
                    yield scrapy.Request(article_url, callback=self.parse);
            if (url_status["init"] == True):
                #for i in range(2, self.nr_page + 1):
                next_index_page = url_status["payload"]["current_page"] + 1
                start_page = url_status["payload"]["start_page"]
                end_page = url_status["payload"]["end_page"];
                for i in range(next_index_page, end_page + 1):
                    next_page = response.css('li.page' + str(i));
                    if len(next_page) == 0:
                        print("Index page " + url + " does not have page " + str(i));
                        continue;
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
                article_content = response.css('div.view_con').css('*::text');
                if (len(article_content) == 0):
                    print("Empty div.content");
            for p in article_content:
                article_str += p.extract();
            article_dict["content"] = article_str;
            url_status['status'] = 'done';
            yield article_dict;
        else:
            print("Unknown type of page " + url);

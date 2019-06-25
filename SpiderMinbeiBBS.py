"""
获取闽北互动论坛的分页招聘信息
"""
import requests
from lxml import etree
import json


class Spider_minbei_bbs(object):

    def __init__(self):
        self.base_url = "http://bbs.np163.net/forum-93-{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.news_list = []

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        data = response.content
        return data

    def parse_data(self, data):
        html = etree.HTML(data)
        title_list = html.xpath('//a[@class="s xst"]/text()')
        url_list = html.xpath('//a[@class="s xst"]/@href')

        for index, news_title in enumerate(title_list):
            news = {}
            news['title'] = news_title
            news['url'] = url_list[index]
            self.news_list.append(news)

    def save_data(self):
        str_news = json.dumps(self.news_list)
        with open("minbeiBBS.json", "w")as f:
            f.write(str_news)

    def run(self):
        for page in range(1, 3):
            url = self.base_url.format(str(page))
            data = self.get_response(url)
            self.parse_data(data)
        self.save_data()


Spider_minbei_bbs().run()

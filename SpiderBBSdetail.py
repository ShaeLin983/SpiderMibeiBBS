"""
获取每个招聘的详情页信息：招聘标题-详情-对应帖子的地址
并生成csv表格文件
"""
import requests
import json
from lxml import etree


class SpiderBBSdetail():

    def __init__(self):
        self.base_index_url = "http://bbs.np163.net/forum-93-{}.html"
        self.base_detail_url = "http://bbs.np163.net/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.content_list = []
        self.detail_url_list = []

    # 发送访问请求
    def get_response(self, url):
        response = requests.get(url, headers=self.headers)
        data = response.content
        return data

    # 解析首页数据，获取所有招聘帖子的详情页地址
    def get_detail_url_list(self, data):
        html = etree.HTML(data)
        self.detail_url_list = html.xpath('//a[@class="s xst"]/@href')

    # 解析详情页数据，获取详情页信息：招聘标题-详情-对应帖子的地址
    def parse_detail_data(self, data):

        html = etree.HTML(data)
        module = html.xpath('//h1[@class="ts"]/a/text()')[0]

        title = html.xpath('//span[@id="thread_subject"]/text()')[0]
        url = html.xpath('//head/link[@rel="canonical"]/@href')[0]
        full_title = module + title
        content = html.xpath('//td[@class="t_f"]//text()')

        # 清洗数据，去除json里的\r\n和空字符串，并把字符串数组拼接成一个字符串
        result = [x.strip('\r\n') for x in content if x.strip() != ""]
        final_result = ''.join(result)

        full_data = {
            "title": full_title,
            "content": final_result,
            "detail url": url
        }
        self.content_list.append(full_data)

    # 保存详情页数据
    def sava_data(self):
        str_content = json.dumps(self.content_list)
        with open("detail.json", "w")as f:
            f.write(str_content)

    def run(self):

        # 请求主页1-3页的内容，并解析出详情页地址
        for page in range(1, 3):
            index_url = self.base_index_url.format(page)
            index_data = self.get_response(index_url)
            self.get_detail_url_list(index_data)

            # 解析详情页信息
            for detail_url in self.detail_url_list:
                full_detail_url = self.base_detail_url + detail_url
                detail_data = self.get_response(full_detail_url)
                self.parse_detail_data(detail_data)

        # 保存信息
        self.sava_data()


SpiderBBSdetail().run()

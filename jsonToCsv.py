"""
把json文件转换成csv文件
"""

import csv
import json


class json_to_csv():

    def __init__(self):
        self.json_file = open("detail.json", "r")
        self.csv_file = open("detail_BBS.csv", "w", encoding='utf-8')
        self.data_list = json.load(self.json_file)

    # 提出json文件的表头
    def abstract_json_thread(self):
        sheet_title = self.data_list[0].keys()
        print(sheet_title)
        return sheet_title

    # 提取表的内容
    def abstract_json_content(self):
        sheet_content_list = []
        for content in self.data_list:
            sheet_content_list.append(content.values())
        print(sheet_content_list)
        return sheet_content_list

    # 写入表头和表的内容
    def write_csv(self, sheet_title, sheet_content_list):
        writer = csv.writer(self.csv_file)
        writer.writerow(sheet_title)
        writer.writerows(sheet_content_list)

    #关闭两个文件
    def close_file(self):
        self.json_file.close()
        self.csv_file.close()

    def run(self):
        thread = self.abstract_json_thread()
        content = self.abstract_json_content()
        self.write_csv(thread, content)
        self.close_file()

json_to_csv().run()

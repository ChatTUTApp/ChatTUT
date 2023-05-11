import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import datetime

# Webページを取得して解析する
url_list = \
[
    "https://pus-pass.com/classwork/class_list?school-year=1&classroom=&period=&select=&division=&keyword=&keyword_teacher=&time_cord=&checked=1"
]

# 保存先ファイル
file_name = "data/homepage.txt"
f = open(file_name, mode='a', encoding='utf-8')

for url in url_list:
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    # 各タグを検索して、その文字列を取得
    tag_list = soup.select("meta")
    f.write("\n講義情報\n" + url + "\n")
    for text in tag_list:
        content = text.get("content")
        print(content)
        f.write(content + "\n")

    tag_list = soup.select("p")
    for text in tag_list:
        print(text.text)
        f.write(text.text + "\n")

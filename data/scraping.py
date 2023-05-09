import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import datetime

# Webページを取得して解析する
url_list = \
[
    "https://www.tut.ac.jp/university/faculty/me/post_62.html",
    "https://www.tut.ac.jp/university/faculty/me/post_88.html",
    "https://www.tut.ac.jp/university/faculty/me/666.html",
    "https://www.tut.ac.jp/university/faculty/me/72.html",
    "https://www.tut.ac.jp/university/faculty/me/749.html",
    "https://www.tut.ac.jp/university/faculty/me/746.html",
    "https://www.tut.ac.jp/university/faculty/me/post_135.html",
    "https://www.tut.ac.jp/university/faculty/me/content_2.html",
    "https://www.tut.ac.jp/university/faculty/me/83.html",
    "https://www.tut.ac.jp/university/faculty/me/33.html",
    "https://www.tut.ac.jp/university/faculty/me/11.html",
    "https://www.tut.ac.jp/university/faculty/me/16.html",
    "https://www.tut.ac.jp/university/faculty/me/21.html",
    "https://www.tut.ac.jp/university/faculty/me/726.html",
    "https://www.tut.ac.jp/university/faculty/me/565.html",
    "https://www.tut.ac.jp/university/faculty/me/82.html",
    "https://www.tut.ac.jp/university/faculty/me/post_12.html",
    "https://www.tut.ac.jp/university/faculty/me/post_38.html",
    "https://www.tut.ac.jp/university/faculty/me/post_112.html",
    "https://www.tut.ac.jp/university/faculty/me/post_105.html",
    "https://www.tut.ac.jp/university/faculty/me/khoo_pei_loon.html",
    "https://www.tut.ac.jp/university/faculty/me/post_83.html",
    "https://www.tut.ac.jp/university/faculty/me/post_97.html",
    "https://www.tut.ac.jp/university/faculty/me/post_116.html",
    "https://www.tut.ac.jp/university/faculty/me/post_6.html",
    "https://www.tut.ac.jp/university/faculty/me/post_120.html",
    "https://www.tut.ac.jp/university/faculty/me/post_85.html",
    "https://www.tut.ac.jp/university/faculty/eiiris/667.html"
]

# 保存先ファイル
file_name = "data/homepage.txt"
f = open(file_name, mode='a', encoding='utf-8')

for url in url_list:
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    # 各タグを検索して、その文字列を取得
    tag_list = soup.select("meta")
    f.write("\n教員情報\n" + url + "\n")
    for text in tag_list:
        content = text.get("content")
        print(content)
        f.write(content + "\n")

    tag_list = soup.select("p")
    for text in tag_list:
        print(text.text)
        f.write(text.text + "\n")


# url = "https://www.tut.ac.jp/university/faculty/me/14.html"
# html = requests.get(url)
# soup = BeautifulSoup(html.content, "html.parser")

# # 保存先ファイル
# file_name = "data/homepage.txt"
# f = open(file_name, mode='a', encoding='utf-8')

# # 各タグを検索して、その文字列を取得
# tag_list = soup.select("meta")
# f.write("\n教員情報\n" + url + "\n")
# for text in tag_list:
#     content = text.get("content")
#     print(content)
#     f.write(content + "\n")

# tag_list = soup.select("p")
# for text in tag_list:
#     print(text.text)
#     f.write(text.text + "\n")
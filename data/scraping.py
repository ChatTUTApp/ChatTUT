import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import datetime

# Webページを取得して解析する
url = "https://www.tut.ac.jp/"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

# 保存先ファイル
file_name = "data/homepage.txt"
f = open(file_name, 'w', encoding='utf-8')

# 各タグを検索して、その文字列を取得
tag_list = soup.select("p")
for text in tag_list:
    print(text.text)
    f.write(text.text+"\n")
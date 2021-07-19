import requests
from bs4 import BeautifulSoup

# Webページを取得して解析する
load_url = "https://baseball-data.com/"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

# IDで検索して、そのタグの中身を表示する
chap2 = soup.find(class_="standings")    # idが「chap2」の範囲の要素を表示
for element in chap2.find_all("td"):    # その中のtdタグの文字列を表示
  print(chap2)

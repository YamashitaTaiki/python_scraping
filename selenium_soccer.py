from selenium import webdriver
import sys
import time
import chromedriver_binary
import re
from bs4 import BeautifulSoup
import pandas as pd
import json

# ドライバーを得る
# ChromeOptionsを設定
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
# options.add_argument('--proxy-server="direct://"')
# options.add_argument('--proxy-bypass-list=*')
# options.add_argument('--start-maximized')
# options.add_argument('--kiosk')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(2)

# サッカー統計画面に移動
url_login = "https://www.premierleague.com/stats/top/players"
driver.get(url_login)
print("統計画面にアクセスしました。")

# driver.find_element_by_id("top-team-stats-summary-grid")
# ソースコードを取得
html = driver.page_source

# HTMLをパースする
soup = BeautifulSoup(html, 'html.parser')  # または、'html.parser'

# soccerデータ取得
# print([i.get_text() for i in soup.select('table tr td:nth-child(3)', limit=20)])


# 1行目 Premier League Player Stats
# Json出力するキー値
jsonMap = {}


def createJson(num, css):
    # Json出力するキー値
    jsonKeyMap = {}
    # json作成用リスト
    empty_list = []
    for i in soup.select(
            css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > a.statName'):
        jsonKeyMap["statName"] = i.get_text()
        break
    for i in soup.select(css + ' ul > li:nth-child('
                         + str(num) + ') > div > ul > li.statsHero > div.statInfo > a.statNameSecondary'):
        jsonKeyMap["statNameSecondary"] = i.get_text()
        break
    for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > div.stat'):
        jsonKeyMap["stat"] = str(i.get_text()).replace('\n', '').replace(' ','')
        break
    for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > div.pos'):
        jsonKeyMap["pos"] = i.get_text()
        break
    empty_list.append(jsonKeyMap)

    for index in range(2, 11):
        # Json出力するキー値
        jsonKeyMap2 = {}
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.teamInfo > a.statName'):
            jsonKeyMap2["statName"] = i.get_text()
            break
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.teamInfo > a.statNameSecondary'):
            jsonKeyMap2["statNameSecondary"] = i.get_text()
            break
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.stat'):
            jsonKeyMap2["stat"] = str(i.get_text()).replace('\n', '').replace(' ','')
            break
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.pos'):
            jsonKeyMap2["pos"] = i.get_text()
            break
        empty_list.append(jsonKeyMap2)
    return empty_list


# Premier League Player Stats
jsonMap["Goal"] = createJson(1,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
jsonMap["Assists"] = createJson(2,
                                '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
jsonMap["Passes"] = createJson(3,
                               '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
jsonMap["Minuter player"] = createJson(4,
                                       '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')

# Attack
jsonMap["shots"] = createJson(1,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
jsonMap["hit woodwork"] = createJson(2,
                                     "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
jsonMap["through balls"] = createJson(3,
                                      "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
jsonMap["crosses"] = createJson(4,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")

# Defence
jsonMap["tackles"] = createJson(1,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
jsonMap["blocks"] = createJson(2,
                               "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
jsonMap["clearances"] = createJson(3,
                                   "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
jsonMap["head clearances"] = createJson(4,
                                        "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")

# Goalkeeper
jsonMap["Clean Sheets"] = createJson(1,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
jsonMap["Saves"] = createJson(2,
                               "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
jsonMap["Punches"] = createJson(3,
                                   "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
jsonMap["Goals Conceded"] = createJson(4,
                                        "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")

# 辞書オブジェクトをJSONファイルへ出力
with open('mydata.json', mode='wt', encoding='utf-8') as file:
    json.dump(jsonMap, file, ensure_ascii=False, indent=2)

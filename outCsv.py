from selenium import webdriver
import sys
import time
import chromedriver_binary
import re
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv

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
csvList = []

# CSVファイル作成
def createCsv(kind,num, css):
    createList = []
    # json作成用リスト
    empty_list = []
    # 引数の項目を追加する
    empty_list.append(kind)
    for i in soup.select(
            css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > a.statName'):
        empty_list.append(i.get_text())
        break
    for i in soup.select(css + ' ul > li:nth-child('
                         + str(num) + ') > div > ul > li.statsHero > div.statInfo > a.statNameSecondary'):
        empty_list.append(i.get_text())
        break
    for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > div.stat'):
        empty_list.append(str(i.get_text()).replace('\n', '').replace(' ',''))
        break
    for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > div.pos'):
        empty_list.append(i.get_text())
        break
    createList.append(empty_list)

    for index in range(2, 11):
        listData = []
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.teamInfo > a.statName'):
            listData.append(i.get_text())
            break
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.teamInfo > a.statNameSecondary'):
            listData.append(i.get_text())
            break
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.stat'):
            listData.append(str(i.get_text()).replace('\n', '').replace(' ',''))
            break
        for i in soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.pos'):
            listData.append(i.get_text())
            # 引数の項目を追加する
            listData.append(kind)
            break
        if listData != []:
            createList.append(listData)
    return createList


# Premier League Player Stats
csvList = createCsv("Goal",1,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
csvList += createCsv("Assists",2,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
csvList += createCsv("Passes",3,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
csvList += createCsv("Minuter player",4,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')

# Attack
csvList += createCsv("shots",1,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
csvList += createCsv("hit woodwork",2,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
csvList += createCsv("through balls",3,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
csvList += createCsv("crosses",4,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")

# Defence
csvList += createCsv("tackles",1,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
csvList += createCsv("blocks",2,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
csvList += createCsv("clearances",3,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
csvList += createCsv("head clearances",4,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")

# Goalkeeper
csvList += createCsv("Clean Sheets",1,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
csvList += createCsv("Saves",2,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
csvList += createCsv("Punches",3,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
csvList += createCsv("Goals Conceded",4,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")

# 辞書オブジェクトをJSONファイルへ出力
with open('output.csv', mode='wt', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csvList)

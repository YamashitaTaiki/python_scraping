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

# driver.find_element_by_id("top-team-stats-summary-grid")
# ソースコードを取得
html = driver.page_source

# HTMLをパースする
soup = BeautifulSoup(html, 'html.parser')  # または、'html.parser'

# soccerデータ取得
# print([i.get_text() for i in soup.select('table tr td:nth-child(3)', limit=20)])


# 1行目 Premier League Player Stats
csvList = [["position","kind","statName","statNameSecondary","stat","pos"]]

# CSVファイル作成
def createCsv(position,kind,num, css):
    createList = []
    # json作成用リスト
    empty_list = []
    # 引数の項目を追加する
    empty_list.append(position)
    empty_list.append(kind)
    statNameList = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > a.statName')
    empty_list.append(statNameList[0].getText() if statNameList != [] else '')
    statNameSecondaryList = soup.select(css + ' ul > li:nth-child('+ str(num) + ') > div > ul > li.statsHero > div.statInfo > a.statNameSecondary')
    empty_list.append(statNameSecondaryList[0].getText() if statNameSecondaryList != [] else '')
    statList = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > div.stat')
    empty_list.append(str(statList[0].getText() if statList !=[] else '').replace('\n', '').replace(' ', ''))
    posList = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li.statsHero > div.statInfo > div.pos')
    empty_list.append(posList[0].getText() if posList != [] else '')

    createList.append(empty_list)

    for index in range(2, 11):
        listData = []
        statName = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(index) + ') > div.teamInfo > a.statName')
            # 引数の項目を追加する
        listData.append(position)
        listData.append(kind)
        listData.append(statName[0].getText() if statName != [] else '')
        statNameSecondary = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.teamInfo > a.statNameSecondary')
        listData.append(statNameSecondary[0].getText() if statNameSecondary != [] else '')
        stat = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.stat')
        listData.append(str(stat[0].getText() if stat != [] else '').replace('\n', '').replace(' ',''))
        pos = soup.select(css + ' ul > li:nth-child(' + str(num) + ') > div > ul > li:nth-child(' + str(
                index) + ') > div.pos')
        listData.append(pos[0].getText() if pos != [] else '')
        if listData[2] != '':
            createList.append(listData)
    return createList


# Premier League Player Stats
csvList += createCsv("Premier League Player Stats","Goal",1,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
csvList += createCsv("Premier League Player Stats","Assists",2,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
csvList += createCsv("Premier League Player Stats","Passes",3,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')
csvList += createCsv("Premier League Player Stats","Minuter player",4,
                             '#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.\\32 01617PlayerStatsTopPlayers >')

# Attack
csvList += createCsv("Attack","shots",1,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
csvList += createCsv("Attack","hit woodwork",2,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
csvList += createCsv("Attack","through balls",3,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")
csvList += createCsv("Attack","crosses",4,
                              "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.AttackTopPlayers >")

# Defence
csvList += createCsv("Defence","tackles",1,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
csvList += createCsv("Defence","blocks",2,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
csvList += createCsv("Defence","clearances",3,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")
csvList += createCsv("Defence","head clearances",4,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.DefenceTopPlayers >")

# Goalkeeper
csvList += createCsv("Goalkeeper","Clean Sheets",1,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
csvList += createCsv("Goalkeeper","Saves",2,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
csvList += createCsv("Goalkeeper","Punches",3,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")
csvList += createCsv("Goalkeeper","Goals Conceded",4,
                                "#mainContent > div.hasSideNav > div > div:nth-child(2) > section.mainWidget.statsRow.GoalkeeperTopPlayers >")

# 辞書オブジェクトをJSONファイルへ出力
with open('output.csv', mode='wt', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csvList)

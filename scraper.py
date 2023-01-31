from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
driver =  webdriver.Chrome(options=options)

def saver(dictex):
    for key, val in dictex.items():
        val.to_csv("train_data/club_{}.csv".format(str(key)))

    with open("train_data/keys.txt", "w") as f: #saving keys to file
        f.write(str(list(dictex.keys())))

# Array containing each season code on the PL website 2006/2007-2021/2022
seasons = {
  "1992/93": 1, 
  "1993/94": 2, 
  "1994/95": 3, 
  "1995/96": 4, 
  "1996/97": 5, 
  "1997/98": 6, 
  "1998/99": 7, 
  "1999/00": 8, 
  "2000/01": 9, 
  "2001/02": 10, 
  "2002/03": 11, 
  "2003/04": 12, 
  "2004/05": 13, 
  "2005/06": 14, 
  "2006/07": 15, 
  "2007/08": 16, 
  "2008/09": 17, 
  "2009/10": 18, 
  "2010/11": 19, 
  "2011/12": 20, 
  "2012/13": 21, 
  "2013/14": 22, 
  "2014/15": 27, 
  "2015/16": 42,
  "2016/17": 54, 
  "2017/18": 79, 
  "2018/19": 210,
  "2019/20": 274,
  "2020/21": 363,
  "2021/22": 418
}

# Array containing each of the premier league teams and their URL ids
teams = {
  "Arsenal": 1,
  "Aston Villa": 2,
  "Chelsea": 4,
  "Manchester United": 12,
  "Bournemouth": 127,
  "Everton": 7,
  "Brighton & Hove Albion": 131,
  "Brentford": 130,
  "Crystal Palace": 6,
  "Fulham": 34,
  "Leeds United": 9,
  "Southampton": 20,
  "Nottingham Forest": 15,
  "West Ham United": 25,
  "Wolves": 38,
  "Manchester City": 11,
  "Liverpool": 10,
  "Leicester City": 26,
  "Newcastle United": 23, 
  "Tottenham Hotspur": 21
}

# Scrape league stats for each team, for each season
num_seasons = len(seasons)
all_stats = {}
team_position_archive = {}
for team, id in teams.items():
  league_positions = {}

  print(team) # For diagnostic purposes

  # Scrape league position data for team
  url = "https://www.premierleague.com/clubs/" + str(id) + "/club/season-history"
  driver.get(url)
  doc = BeautifulSoup(driver.page_source, "html.parser")

  club_archive = doc.find_all(class_="club-archive")
  for year in club_archive:
    if (year.header is None):
      continue
    year_title = year.header.h2.string.split(" ")[0]
    year_position = year.find(class_="club-archive__description-list").dl.dd

    if year_position.has_attr('class'):
      league_positions[year_title] = '1st'
    else:
      league_positions[year_title] = year_position.string

  # Scrape season stats and append finishing pos as data label
  team_stats = {}
  for year, position in league_positions.items():
    year_data = {}
    url = "https://www.premierleague.com/clubs/" + str(teams[team]) + "/club/stats?se=" + str(seasons[year])
    driver.get(url)
    time.sleep(2) # Page uses JS to render content, so wait for it to update
    doc = BeautifulSoup(driver.page_source, "html.parser")
    normal_stats = doc.find_all(class_="normalStat")
    for stat in normal_stats:
      title = stat.find(class_="allStatContainer").attrs["data-stat"]
      value = stat.find(class_="allStatContainer").string
      year_data[title] = value
      year_data["position"] = league_positions[year] # add label
    team_stats[year] = year_data

  df = pd.DataFrame(team_stats)
  all_stats[team] = df.T

saver(all_stats)
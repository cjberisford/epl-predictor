from bs4 import BeautifulSoup
import requests

url = "https://www.premierleague.com/clubs/12/club/stats"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

stats_tables = doc.find_all(class_="statsListBlock")
attacking_stats = doc.find_all(class_="normalStat")

for stat in attacking_stats:
  title = stat.find(class_="allStatContainer").attrs["data-stat"]
  value = stat.find(class_="allStatContainer").string
  print(title, value)
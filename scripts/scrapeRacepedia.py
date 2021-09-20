############
# DISCLAIMER
# Every "scraper" contains the risk to 'overload' a website/server.
# Thus, be aware to not do such things and act responsible.
############

# TODOs
# Replace this script with a python-programm that takes an address as argument
# and handles the processes respectively

# Module import
import requests
import csv
import random
import time
import pandas as pd
from bs4 import BeautifulSoup

# Get content
url = "https://frankfurt-city-triathlon-2021.racepedia.de/ergebnisse/3690"
response = requests.get(url)

# Parse rows from html
html = BeautifulSoup(response.text, 'html.parser')
table = html.find("table")
rows = table.findAll("tr")
urlsDetail = list()
for row in rows:
    urlsDetail.append(str(row.get("data-fancybox")))

# Adjust url
url = url.split("/ergebnisse")[0]

# Init data
data = list()

# Loop over results and parse them respectively
for urlDetail in urlsDetail:
    # Check if urlDetail is valid
    if urlDetail.startswith("/ergebnisse/resultdetail"):
        # Adjust urlDetail and get content
        respDetail = requests.get(url + urlDetail)
        htmlDetail = BeautifulSoup(respDetail.text, 'html.parser')

        # Parse output
        info = htmlDetail.find("div", {"class": "info"})

        # List in list
        dataDetail = {
                'startNum': '',
                'name': '',
                'rank': '',
                'sex': '',
                'age': '',
                'oTime': '',
                'nTime': '',
                'swim': '',
                'change 1': '',
                'bike': '',
                'change 2': '',
                'run': '',
                'finish swim': '',
                'finish change 1': '',
                'finish bike': '',
                'finish change 2': '',
                'finish run': '',
                }

        # TODO:
        # This whole thing does not make me happy :(
        # To much conditions, to little generic

        # Header
        cf = str(info.find("div", {"class": "cf"}).text)
        startNum, name = ["" for _ in range(2)]
        dataDetail["startNum"] = cf.split(",", 1)[0].strip()
        dataDetail["name"] = cf.split(",", 1)[1].strip()

        # Left side
        left = str(info.find("div", {"class": "left"}).text).splitlines()
        for item in left:
            it = item.lstrip()
            if it.startswith('Gesamtplatz'):
                dataDetail["rank"] = it.split(":")[1]
            elif it.startswith('Platz Geschlecht'):
                dataDetail["sex"] = it.split(":")[1]
            elif it.startswith('Altersklassenplatz'):
                dataDetail["age"] = it.split(":")[1]
            elif it.startswith('Gesamtzeit'):
                dataDetail["oTime"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Nettozeit'):
                dataDetail["nTime"] = it.split(":", 1)[1][:-2]

        # Right side
        right = str(info.find("div", {"class": "right"}).text).splitlines()
        for item in right:
            it = item.lstrip()
            if it.startswith('Schwimmen'):
                dataDetail["swim"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Wechsel 1'):
                dataDetail["change 1"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Radfahren'):
                dataDetail["bike"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Wechsel 2'):
                dataDetail["change 2"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Laufen'):
                dataDetail["run"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Beim Schwimmende'):
                dataDetail["finish swim"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Nach Wechsel 1'):
                dataDetail["finish change 1"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Nach Radfahren'):
                dataDetail["finish bike"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Beim Laufstart'):
                dataDetail["finish change 2"] = it.split(":", 1)[1][:-2]
            elif it.startswith('Ziel'):
                dataDetail["finish run"] = it.split(":", 1)[1][:-2]

        data.append(dataDetail)

        # sleep random amount of seconds to not overload their server
        sleepTime = random.randint(1, 5)
        time.sleep(sleepTime)

# Create dataframe and export data to csv
df = pd.DataFrame(data)
df.to_csv("file.csv", index=False, sep=';')

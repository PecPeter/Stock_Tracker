import string
import sqlite3
import requests
from bs4 import BeautifulSoup
import csv

trackerDB = "stock_ticker.db"
conn = sqlite3.connect(trackerDB)
cur = conn.cursor()

# Get the list of the current tables that exist in the db
# If the ticker_list table doesn't exist, generate it
cur.execute("SELECT name FROM sqlite_master;")
tableList = cur.fetchall()
tableExists = False
for tableItr in tableList :
    if tableItr[0] == "ticker_list" :
        tableExists = True

if tableExists == True :
    # Delete the ticker_list table to refresh all the values
    cur.execute("DROP TABLE ticker_list;")
cur.execute("CREATE TABLE ticker_list(" \
            "NAME TEX, TICKER TEXT, EXCHANGE TEXT);")

# This updates the TSX tickers
# Iterate through every character in the alphabet to find all the tickers
for alphaItr in string.ascii_uppercase :
    print("Searching TSX for letter: " + alphaItr)
    alphaString = "&SearchKeyword=" + alphaItr
    urlTSX = "http://www.tmxmoney.com/TMX/HttpController?" \
             "GetPage=ListedCompanyDirectory" \
             "&SearchCriteria=Name&SearchType=StartWith&SearchIsMarket=Yes&" \
             "Market=T&Language=en"
    req = requests.get(urlTSX + alphaString)

    tree = BeautifulSoup(req.content, "lxml")
    pageCountString = tree.select("div.fullTableWrapper table td[rowspan=\"2\"]")
    maxPageCount = 1
    if len(pageCountString) != 0 :
        pageCountString = pageCountString[0].text.split()
        maxPageCount = int(pageCountString[len(pageCountString)-1])

    # Iterate through all the pages for the letter
    for pageItr in range(1, maxPageCount + 1) :
        print("    Page: " + str(pageItr) + " of " + str(maxPageCount))
        pageString = "&Page=" + str(pageItr)
        req = requests.get(urlTSX + alphaString + pageString)
        tree = BeautifulSoup(req.content, "lxml")
        infoTable = tree.select("table.tablemaster td.td-left-padding a")
        tickerList = []
        for index in range(0, int(len(infoTable)/2)-1) :
            tickerName = infoTable[index*2].text
            ticker = infoTable[index*2+1].text
            tickerTuple = (tickerName, ticker, "TSX")
            tickerList.append(tickerTuple)
        cur.executemany("INSERT INTO ticker_list VALUES (?,?,?);", tickerList)

# This updates the NASDAQ, NYSE, and AMEX tickers
# The NASDAQ maintains 3 csv files that contain unique tickers for the 3
# different stock exchanges. Read from each file, and update the database
csvURL = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&render=download&exchange="
s = requests.Session()
exchangeList = ["NASDAQ", "NYSE", "AMEX"]
for exchangeItr in exchangeList :
    print("Searching " + exchangeItr + " exchange for tickers.")
    download = requests.Session().get(csvURL + exchangeItr)
    decoded_content = download.content.decode("utf-8")
    cr = csv.reader(decoded_content.splitlines(), delimiter=",")
    my_list = list(cr)
    tickerList = []
    for row in my_list :
        tickerName = row[1]
        ticker = row[0]
        tickerTuple = (tickerName, ticker, exchangeItr)
        tickerList.append(tickerTuple)
    cur.executemany("INSERT INTO ticker_list VALUES (?,?,?);", tickerList)
conn.commit()

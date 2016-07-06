import string
import sqlite3
import requests
from bs4 import BeautifulSoup
import csv

from sqlCommand import exchangeEntry

def populate_TSX (connection) :
    # This updates the TSX tickers
    # Iterate through every character in the alphabet to find all the tickers
    cur = connection

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
            cur.executemany(exchangeEntry.format("exchangeTable_TSX"), tickerList)
    connection.commit()

def populate_NASDAQ (connection) :
    populate_amer_exchange(connection,"NASDAQ")

def populate_NYSE (connection) :
    populate_amer_exchange(connection,"NYSE")

def populate_AMEX (connection) :
    populate_amer_exchange(connection,"AMEX")

def populate_amer_exchange (connection, exchange) :
    cur = connection.cursor()
    csvURL = "http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&render=download&exchange="
    s = requests.Session()
    print("Searching " + exchange + " exchange for tickers.")
    download = requests.Session().get(csvURL + exchange)
    decoded_content = download.content.decode("utf-8")
    cr = csv.reader(decoded_content.splitlines(), delimiter=",")
    my_list = list(cr)
    tickerList = []
    for row in my_list :
        tickerName = row[1]
        ticker = row[0]
        tickerTuple = (tickerName, ticker, exchange)
        tickerList.append(tickerTuple)
    cur.executemany(exchangeEntry.format("exchangeTable_"+exchange), tickerList)
    connection.commit()

import sqlite3
import requests
from bs4 import BeautifulSoup
import csv

import sqlCommand
import utilFunc

def populate_stock (stockSym, exchange, hpTableName, fnclTableName,
                    updateFrom, updateTo, connection) :
    # Grab the info for the provided stock
    # Alter the stockSym if needed
    if exchange == "TSX" :
        stockSym += ".TO"
    fromDate = utilFunc.convert_int_to_date(updateFrom)
    toDate = utilFunc.convert_int_to_date(updateTo)
    # Construct the URL to grab the csv file from for the hp table
    csvURL = "http://chart.finance.yahoo.com/table.csv?s=" + stockSym + "&a=" + \
             str(fromDate.month - 1) + "&b=" + str(fromDate.day) + "&c=" + \
             str(fromDate.year) + "&d=" + str(toDate.month - 1) + "&e=" + \
             str(toDate.day) + "&f=" + str(toDate.year) + "&g=d&ignore=.csv"

    # Load the csv file and read it into the hp table
    download = requests.get(csvURL)
    decoded_content = download.content.decode("utf-8")
    cr = csv.reader(decoded_content.splitlines(), delimiter = ",")
    my_list = list(cr)
    hpList = []
    firstRow = True
    for row in my_list :
        if firstRow == True :
            firstRow = False
        else :
            date = utilFunc.convert_str_to_int(row[0])
            openPrice = float(row[1])
            highPrice = float(row[2])
            lowPrice = float(row[3])
            closePrice = float(row[4])
            volume = int(row[5])
            rowTuple = (date,openPrice,highPrice,lowPrice,closePrice,volume)
            hpList.append(rowTuple)
    connection.executemany(sqlCommand.hpTableEntry.format(hpTableName),hpList)
    connection.commit()

def find_tracked_stock (stockId, cursor) :
    # The stockid can be the symbol or the name of the stock
    matchedStockList = []
    cursor.execute(sqlCommand.searchStockTableSym.format("trackedStockTable"),
                   (stockId,))
    tmpMatchedStockList = cursor.fetchall()
    for listItr in tmpMatchedStockList :
        matchedStockList.append(listItr)
    cursor.execute(sqlCommand.searchStockTableName.format("trackedStockTable"),
                   (stockId,))
    tmpMatchedStockList = cursor.fetchall()
    for listItr in tmpMatchedStockList :
        matchedStockList.append(listItr)

    return matchedStockList

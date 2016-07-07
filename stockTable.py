import sqlite3

import sqlCommand

def populate_stock (stockSym, stockName, exchange, updateFrom, updateTo, connection) :
    # Grab the info for the provided stock
    print("Populate stock")

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

import datetime
import sqlite3

import sqlCommand
import exchangeTable

def create_database (databasePath) :
    conn = sqlite3.connect(databasePath)
    curs = conn.cursor()

    # Create all the necessary tables now
    curs.execute(sqlCommand.createInfoTable.format("infoTable"))
    curs.execute(sqlCommand.createExchangeTable.format("exchangeTable_TSX"))
    curs.execute(sqlCommand.createExchangeTable.format("exchangeTable_NASDAQ"))
    curs.execute(sqlCommand.createExchangeTable.format("exchangeTable_NYSE"))
    curs.execute(sqlCommand.createExchangeTable.format("exchangeTable_AMEX"))
    conn.commit()

    # Populate the tables
    exchangeTable.populate_TSX(conn)
    exchangeTable.populate_NASDAQ(conn)
    exchangeTable.populate_NYSE(conn)
    exchangeTable.populate_AMEX(conn)
    date = datetime.date.today()
    date = (date.year*10000) + (date.month*100) + date.day
    actionList = [("exchangeTable_TSX", date), \
                  ("exchangeTable_NASDAQ", date), \
                  ("exchangeTable_NYSE", date), \
                  ("exchangeTable_AMEX", date)]
    curs.executemany(sqlCommand.infoTableEntry.format("infoTable"), actionList)
    conn.commit()
    conn.close()

def check_stock (stockId, cursor) :
    # The stockid can be the symbol or the name of the stock
    matchedTickerList = []
    cursor.execute(searchExchangeName, "exchangeTable_TSX", stockId)
    matchedTickerList.append(cursor.fetchall())
    cursor.execute(searchExchangeSym, "exchangeTable_TSX", stockId)
    matchedTickerList.append(cursor.fetchall())

    cursor.execute(searchExchangeName, "exchangeTable_NASDAQ", stockId)
    matchedTickerList.append(cursor.fetchall())
    cursor.execute(searchExchangeSym, "exchangeTable_NASDAQ", stockId)
    matchedTickerList.append(cursor.fetchall())

    cursor.execute(searchExchangeName, "exchangeTable_NYSE", stockId)
    matchedTickerList.append(cursor.fetchall())
    cursor.execute(searchExchangeSym, "exchangeTable_NYSE", stockId)
    matchedTickerList.append(cursor.fetchall())

    cursor.execute(searchExchangeName, "exchangeTable_AMEX", stockId)
    matchedTickerList.append(cursor.fetchall())
    cursor.execute(searchExchangeSym, "exchangeTable_AMEX", stockId)
    matchedTickerList.append(cursor.fetchall())

    return matchedTickerList

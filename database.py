import datetime
import sqlite3

import sqlCommand
import stockTable
import exchangeTable
import utilFunc

def create_database (databasePath) :
    print("Generating database: " + databasePath)
    conn = sqlite3.connect(databasePath)
    curs = conn.cursor()

    # TODO: Make a list that contains the different table names so that this can
    # be iterated over during generation. Can contain table names, urls,
    # strings for variables when searching for them, etc...

    # Create all the exchange tables
    print("   Creating database tables")
    conn.execute(sqlCommand.createExchangeInfoTable.format("exchangeInfoTable"))
    conn.execute(sqlCommand.createExchangeTable.format("exchangeTable_TSX"))
    conn.execute(sqlCommand.createExchangeTable.format("exchangeTable_NASDAQ"))
    conn.execute(sqlCommand.createExchangeTable.format("exchangeTable_NYSE"))
    conn.execute(sqlCommand.createExchangeTable.format("exchangeTable_AMEX"))
    conn.commit()

    # Create the tracked stock table
    conn.execute(sqlCommand.createTrackedStockTable.format("trackedStockTable"))
    conn.commit()

    # Populate the tables
    print("       Populating TSX Exchange Stock Table")
    exchangeTable.populate_TSX(conn)
    print("       Populating NASDAQ Exchange Stock Table")
    exchangeTable.populate_NASDAQ(conn)
    print("       Populating NYSE Exchange Stock Table")
    exchangeTable.populate_NYSE(conn)
    print("       Populating AMEX Exchange Stock Table")
    exchangeTable.populate_AMEX(conn)
    date = utilFunc.convert_date_to_int(datetime.date.today())
    actionList = [("exchangeTable_TSX", date), \
                  ("exchangeTable_NASDAQ", date), \
                  ("exchangeTable_NYSE", date), \
                  ("exchangeTable_AMEX", date)]
    conn.executemany(sqlCommand.exchangeInfoTableEntry.format("exchangeInfoTable"), actionList)
    conn.commit()
    conn.close()

def track_stock (stockId, connection) :
    # Check if the stockId matches a name or symbol
    cursor = connection.cursor()
    matchedStockList = exchangeTable.find_exchange_stock(stockId, cursor)
    if len(matchedStockList) == 0 :
        print("Did not find a stock with a name/symbol of: " + stockId)
        return False
    elif len(matchedStockList) > 1 :
        print("Found " + str(len(matchedStockList)) + " matching stocks:")
        for listItr in matchedStockList :
            print("    Stock Name: " + listItr[0])
            print("    Stock Sym:  " + listItr[1])
            print("    Exchange:   " + listItr[2] + "\n")
        return False

    # Found single stock
    stockSym = matchedStockList[0][0]
    stockName = matchedStockList[0][1]
    exchange = matchedStockList[0][2]

    print("\nGathering information for:")
    print("    Stock Name: " + stockName)
    print("    Stock Sym:  " + stockSym)
    print("    Exchange:   " + exchange + "\n")

    # Check if the stock is already being tracked
    cursor.execute(sqlCommand.searchStockTableSym.format("trackedStockTable"),
                   (stockSym,))
    if len(cursor.fetchall()) != 0 :
        print("The selected stock is already being tracked.")
        return True

    updateTo = datetime.date.today()
    updateFrom = datetime.date(updateTo.year-1,updateTo.month,updateTo.day)
    updateTo = utilFunc.convert_date_to_int(updateTo)
    updateFrom = utilFunc.convert_date_to_int(updateFrom)

    # Stock is not being tracked already, generate the stock specific
    # entries/tables
    connection.execute(sqlCommand.trackedStockTableEntry.format("trackedStockTable"),
                       (stockSym,stockName,exchange,updateFrom,updateTo))
    hpTableName = utilFunc.gen_hp_table_name(stockSym, exchange)
    fnclTableName = utilFunc.gen_fncl_table_name(stockSym, exchange)
    connection.execute(sqlCommand.createHPTable.format(hpTableName))
    connection.execute(sqlCommand.createFnclTable.format(fnclTableName))
    connection.commit()

    # Populate the tables
    stockTable.populate_stock(stockSym,stockName,exchange,updateFrom,updateTo,connection)
    return True

def untrack_stock (stockId, connection) :
    # Find if the stock is tracked
    cursor = connection.cursor()
    matchedStockList = stockTable.find_tracked_stock(stockId,cursor)
    if len(matchedStockList) == 0 :
        print("Did not find stock with a name/symbol of: " + stockId)
        return False
    elif len(matchedStockList) > 1 :
        print("Found " + str(len(matchedStockList)) + " matching stocks:")
        for listItr in matchedStockList :
            print("    Stock Name: " + listItr[0])
            print("    Stock Sym:  " + listItr[1])
            print("    Exchange:   " + listItr[2] + "\n")
        return False

    # Found single stock
    stockSym = matchedStockList[0][0]
    stockName = matchedStockList[0][1]
    exchange = matchedStockList[0][2]

    print("\nRemoving information for:")
    print("    Stock Name: " + stockName)
    print("    Stock Sym:  " + stockSym)
    print("    Exchange:   " + exchange + "\n")

    # Delete the tables for the stock, and remove the tracked entry
    connection.execute(sqlCommand.deleteStockTableSym.format("trackedStockTable"),
                       (stockSym,))
    hpTableName = utilFunc.gen_hp_table_name(stockSym, exchange)
    fnclTableName = utilFunc.gen_fncl_table_name(stockSym, exchange)
    connection.execute(sqlCommand.dropTable.format(hpTableName))
    connection.execute(sqlCommand.dropTable.format(fnclTableName))

    return True

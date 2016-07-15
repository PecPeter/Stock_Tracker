import sqlite3
import datetime

import sqlCommand

def convert_date_to_int (date) :
    return date.year*10000 + date.month*100 + date.day

def convert_int_to_date (date) :
    year = date // 10000
    month = (date - (year*10000)) // 100
    day = (date - (year*10000) - month*100)
    return datetime.date(year,month,day)

def convert_str_to_int (date) :
    # String format is: YYYY-MM-DD
    tmpDate = datetime.date(int(date[:4]),int(date[5:7]),int(date[8:]))
    return convert_date_to_int(tmpDate)

def gen_hp_table_name (stockSym, exchange) :
    return stockSym + "_" + exchange + "_hp"

def gen_fncl_table_name (stockSym, exchange) :
    return stockSym + "_" + exchange + "_fncl"

def find_stock (stockId, tableList, searchBy, cursor):
    matchedStockList = []
    for tableItr in tableList:
        cursor.execute(sqlCommand.searchTable.format(tableItr[0]),{"col":searchBy,"value":stockId})
#        cursor.execute(sqlCommand.searchStockBySym.format(tableItr[0]))
        for listItr in cursor.fetchall():
            matchedStockList.append(listItr)
    return matchedStockList

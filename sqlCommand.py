#------------------------------------------------------------------------------

# SQL command string to create the tracked stock table
createTrackedStockTable = "CREATE TABLE {} (SYMBOL TEXT COLLATE NOCASE," \
                          "NAME TEXT COLLATE NOCASE," \
                          "EXCHANGE TEXT, TRACKING_FROM INT," \
                          "TRACKING_TO INT);"
# SQL command string to insert new tracked stock entry
trackedStockTableEntry = "INSERT INTO {} VALUES (?,?,?,?,?);"
# SQL command string to search for tracked stock symbol
searchStockTableSym = "SELECT * FROM {} WHERE SYMBOL=?;"
# SQL command string to search for tracked stock by name
searchStockTableName = "SELECT * FROM {} WHERE NAME=?;"
# SQL command string to delete row from symbol
deleteStockTableSym = "DELETE FROM {} WHERE SYMBOL=?;"
# SQL command string to delete row from name
deleteStockTableName = "DELETE FROM {} WHERE NAME=?;"

#------------------------------------------------------------------------------

# Every tracked stock will have the following tables:
# SQL command string to create a stocks' historical price table
createHPTable = "CREATE TABLE {} (DATE INT PRIMARY KEY," \
                "OPEN REAL, HIGH REAL, LOW REAL, CLOSE REAL, VOLUME INT);"
hpTableEntry = "INSERT INTO {} VALUES (?,?,?,?,?,?);"
# SQL command string to create a stocks' financial data table
createFnclTable = "CREATE TABLE {} (DATE INT PRIMARY KEY);"

#------------------------------------------------------------------------------

createExchangeInfoTable = "CREATE TABLE {} (TABLE_NAME TEXT, UPDATED_DATE INT);"
exchangeInfoTableEntry = "INSERT INTO {} VALUES (?,?);"

#------------------------------------------------------------------------------

createExchangeTable = "CREATE TABLE {} (SYMBOL TEXT COLLATE NOCASE," \
                      "NAME TEXT COLLATE NOCASE," \
                      "EXCHANGE TEXT);"
exchangeEntry = "INSERT INTO {} VALUES (?,?,?);"
searchExchangeName = "SELECT * FROM {} WHERE NAME=?;"
searchExchangeSym = "SELECT * FROM {} WHERE SYMBOL=?;"

#------------------------------------------------------------------------------

dropTable = "DROP TABLE IF EXISTS {};"
searchTable = "SELECT * FROM {} WHERE :col=:value;"
searchStockByName = "SELECT * FROM {} WHERE NAME=?;"
searchStockBySym = "SELECT * FROM {} WHERE SYMBOL=?;"

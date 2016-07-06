createInfoTable = "CREATE TABLE {} (TABLE_NAME TEXT, UPDATED_DATE INT);"
infoTableEntry = "INSERT INTO {} VALUES (?,?);"

createHPTable = "CREATE TABLE {} (DATE PRIMARY KEY INT," \
                "OPEN INT, HIGH INT, LOW INT, CLOSE INT, VOLUME INT);"
createFnclTable = "CREATE TABLE {} (DATE PRIMARY KEY INT);"

createExchangeTable = "CREATE TABLE {} (SYMBOL TEXT, NAME TEXT, EXCHANGE TEXT);"
searchExchangeName = "SELECT * FROM {} WHERE NAME=?;"
searchExchangeSym = "SELECT * FROM {} WHERE SYMBOL=?;"
exchangeEntry = "INSERT INTO {} VALUES (?,?,?);"

dropTable = "DROP TABLE ?;"

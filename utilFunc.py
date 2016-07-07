import datetime

def convert_date_to_int (date) :
    return date.year*10000 + date.month*100 + date.day

def convert_int_to_date (date) :
    year = date // 10000
    month = (date - (year*10000)) // 100
    day = (date - (year*10000) - month*100)
    return datetime.date(year,month,day)

def gen_hp_table_name (stockSym, exchange) :
    return stockSym + "_" + exchange + "_hp"

def gen_fncl_table_name (stockSym, exchange) :
    return stockSym + "_" + exchange + "_fncl"

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(curPath)
sys.path.append(rootPath)

class Config:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.QUTOE_PATH = rootPath + "/data/quote.csv"
        self.ZZ800_DATA = rootPath + '/data/800_data.csv'

        self.RECORDS_PATH = rootPath + "/data/records.csv"
        self.NAV_PATH = rootPath + "/data/nav_sample.csv"
        self.INDUTRY_PATH = rootPath + '/data/industry.csv'
        self.INDUSTRYQUOTE_PATH = rootPath + '/data/industry_quote.xlsx'
        self.TRADING_DAY = rootPath + '/data/tradingday.csv'

        self.current_date = '2017-01-01'

config = Config()
import sys
import os
import pandas as pd

class Config:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):

        self.rootPath = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]

        # self.QUTOE_PATH = self.rootPath + "/data/quote.csv"  # 股票行情
        # self.RECORDS_PATH = self.rootPath + "/data/records.csv" # 大v的操作记录
        # self.NAV_PATH = self.rootPath + "/data/nav_sample.csv" # 大V的表现
        # self.INDUTRY_PATH = self.rootPath + '/data/industry.csv' # 行业信息
        # self.INDUSTRYQUOTE_PATH = self.rootPath + '/data/industry_quote.xlsx'  # 行业行情

        self.TRADING_DAY = self.rootPath + '/data/trading_day.csv'
        self.ZZ800_DATA = self.rootPath + '/data/800_data.csv'
        self.ZZ800_CODES = self.rootPath + '/data/800_codes.csv'
        self.ZZ800_MARKET_RATIO = self.rootPath + '/data/800_ratio.csv'

        self.result = self.rootPath + '/pic/nav.jpg'

        self.start_date = pd.to_datetime('2018-01-01')
        self.train_start = pd.to_datetime('2017-09-01')
        self.train_end = pd.to_datetime('2017-12-31')

        self.episode = 10
        # self.train_days = 100

config = Config()
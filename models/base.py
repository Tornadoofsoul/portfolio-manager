#encoding:utf-8
import os
import sys
import pandas as pd
from datetime import timedelta
from models.config import config

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(curPath)
sys.path.append(rootPath)

class Base():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    # 大v的操作记录
    def load_records_csv(self):
        print('load records data....')
        df = pd.read_csv(config.RECORDS_PATH, parse_dates=['Updated'])
        df["Updated"] = df["Updated"].apply(lambda x: pd.to_datetime(x))
        return df

    # 股票行情
    def load_quote_csv(self):
        print('load quote data....')
        df = pd.read_csv(config.QUTOE_PATH, parse_dates=['TradingDay'])
        return df

    # 大V的表现
    def load_nav_csv(self):
        print('load nav data....')
        df = pd.read_csv(config.NAV_PATH, parse_dates=['NavDate'])
        df["NavDate"] = df["NavDate"].apply(lambda x: pd.to_datetime(x))
        return df

    # 行业信息
    def load_industry_csv(self):
        print('load industry data....')
        df = pd.read_csv(config.INDUTRY_PATH)
        return df

    # 行业行情
    def load_industry_quote_xlsx(self):
        print('load industry quote data...')
        df = pd.read_excel(config.INDUSTRY_QUOTE_PATH)
        df.columns = df.iloc[0, :].apply(lambda x: x[:-4]).values
        df = df.iloc[2:]
        df.index.names = ['TradingDay']
        df.reset_index(inplace=True)
        return df

    # 交易日
    def load_trading_day_csv(self):
        print('load trading day data....')
        return pd.read_csv(config.TRADING_DAY,  parse_dates=['TradingDate'])

    def load_800_data(self):
        print('load 800 data....')
        return pd.read_csv(config.ZZ800_DATA, parse_dates=['DATE'])

    def make_diff(self):
        # df = self.load_quote_csv()
        # df['diff1'] = df.groupby(['SecuCode'])['Close'].diff()
        # df['diff2'] = df.groupby(['SecuCode'])['diff1'].diff()
        # df.to_csv(config.QUTOE_PATH, index=False)

        df = self.load_800_data()
        df['diff1'] = df.groupby(['CODE'])['CLOSE'].diff()
        df['diff2'] = df.groupby(['CODE'])['diff1'].diff()
        df.to_csv(config.ZZ800_DATA, index=False)

    def get_last_month(self, date, days):
        date_ = str((pd.to_datetime(date) - timedelta(days=days)).date())
        return date_
base = Base()

if __name__ == '__main__':
    base.make_diff()
    print('')
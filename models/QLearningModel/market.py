from random import randrange
from models.config import config
from datetime import timedelta
from models import base
import os
import pandas as pd

class Market():
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.current_date = config.start_date
        self.train_start = config.train_start
        self.train_end = config.train_end

        self.ratios = None
        self.trading_days = None
        self.codes = None
        self.all_data = None
        self._init_all_data()

        self.train_pool = None
        self.test = None
        self.stage = 'Train'
        self._init_train_pool_and_test_data()

        self.current_state = None

    def _init_all_data(self):

        if self.all_data is None:
            print('Init All Data! ', os.getpid())
            self.all_data = pd.read_csv(config.ZZ800_DATA, parse_dates=['DATE'], dtype={'CODE': 'str'})

        self.codes = self.all_data['CODE'].unique()
        self.trading_days = pd.read_csv(config.TRADING_DAY, parse_dates=['DATE'])
        self.ratios = pd.read_csv(config.ZZ800_MARKET_RATIO, parse_dates=['DATE'])

    def _init_train_pool_and_test_data(self):
        self.test = self.all_data[self.all_data['DATE'] >= self.current_date].dropna()
        # train = self.all_data[(self.all_data['DATE'] >= self.previous_date(self.train_end, 7)) &
        #                           (self.all_data['DATE'] <= self.train_end)].dropna()
        if self.stage == 'Train':
            train = self.all_data[(self.all_data['DATE'] >= self.train_start) &
                                  (self.all_data['DATE'] <= self.train_end)].dropna()
            self.train_pool = base.gen_experience_display_pool(train)

    def get_state(self, code=None):
        if self.stage == 'Train':
            data = self.train_pool
            ind = randrange(0, len(data) - 1)
            self.current_state = self.train_pool[ind]
        elif self.stage == 'Test':
            data = self.test[self.test['CODE'] == code]
            data = data.sort_values(ascending=True, by=['DATE'])
            self.current_state = data.iloc[0:2]
        if self.current_state.empty or self.current_state.shape[0] == 1:
            return None, None

        diff1 = round(self.current_state.iloc[0]['diff1'], 1)
        diff2 = round(self.current_state.iloc[0]['diff2'], 1)

        diff1_ = round(self.current_state.iloc[1]['diff1'], 1)
        diff2_ = round(self.current_state.iloc[1]['diff2'], 1)

        s = str(diff1) + ',' + str(diff2)
        s_ = str(diff1_) + ',' + str(diff2_)
        return s, s_

    def get_reward(self, action):
        v1 = self.current_state['CLOSE'].values[0]
        v2 = self.current_state['CLOSE'].values[1]
        reward = (v2 - v1) / v1

        assert str(market.pass_days(market.current_date.date(), 1)) not in str(market.current_state['DATE'])

        if action == 0:
            return 0 - reward
        else:
            return reward

    def pass_days(self, date, nb_day):
        date_ = pd.to_datetime(self.trading_days[self.trading_days['DATE'] > date].head(nb_day).tail(1).values[0][0])
        return date_

    def _pass_a_day(self):
        self.current_date = pd.to_datetime(self.trading_days[self.trading_days['DATE'] > self.current_date].head(1).values[0][0])
        self._init_train_pool_and_test_data()

    def _pass_a_week(self):
        self.current_date = pd.to_datetime(self.trading_days[self.trading_days['DATE'] > self.current_date].head(5).tail(1).values[0][0])
        self._init_train_and_test_data()

    def previous_date(self, date, days):
        date_ = str((pd.to_datetime(date) - timedelta(days=days)).date())
        return date_

    def get_data(self, start_date=None, end_date=None, code=None, pattern_length=30):
        all_data = self.all_data

        if code is not None:
            if start_date == None and end_date != None:
                pattern = all_data[(all_data['CODE'] == code) & (all_data['DATE'] <= end_date)].tail(pattern_length)
            elif start_date != None and end_date == None:
                pattern = all_data[(all_data['CODE'] == code) & (all_data['DATE'] >= start_date)].head(pattern_length)
            elif start_date != None and end_date != None:
                pattern = all_data[
                    (all_data['CODE'] == code) & (all_data['DATE'] <= end_date) & (all_data['DATE'] >= start_date)]
        else:
            if start_date == None and end_date != None:
                pattern = all_data[(all_data['DATE'] <= end_date)].tail(pattern_length)
            elif start_date != None and end_date == None:
                pattern = all_data[(all_data['DATE'] >= start_date)].head(pattern_length)
            elif start_date != None and end_date != None:
                pattern = all_data[(all_data['DATE'] <= end_date) & (all_data['DATE'] >= start_date)]

        return pattern

market = Market()

if __name__ == '__main__':
    print('')
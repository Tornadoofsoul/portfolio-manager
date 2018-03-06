import numpy as np
from models.base import base
from random import randrange
from models.config import config

class Env():
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.done = False
        self.quote = base.load_800_data()

        self.train = self.quote[self.quote['DATE'] <= config.current_date]
        self.train = self.train[self.train['DATE'] >= base.get_last_month(config.current_date, 7)].dropna()
        self.test = self.quote[self.quote['DATE'] > config.current_date]

        self.cur_state = None
        self.test_counter = 0
        print('Train Size:', self.train.shape[0])
        print('Test Size:', self.test.shape[0])

    def get_state(self, code=None):
        if self.stage == 'Train':
            data = self.train
            ind = randrange(0, data.shape[0] - 1)
            self.cur_state = data.iloc[ind: ind + 2]
        else:
            data = self.test[self.test['CODE'] == code]
            self.cur_state = data.iloc[self.test_counter: self.test_counter + 2]
            self.test_counter = self.test_counter + 1

        diff1 = round(self.cur_state.iloc[0]['diff1'], 1)
        diff2 = round(self.cur_state.iloc[0]['diff2'], 1)

        diff1_ = round(self.cur_state.iloc[1]['diff1'], 1)
        diff2_ = round(self.cur_state.iloc[1]['diff2'], 1)

        s = str(diff1) + ',' + str(diff2)
        s_ = str(diff1_) + ',' + str(diff2_)
        return s, s_

    def get_reward(self, action):
        v1 = self.cur_state['CLOSE'].values[0]
        v2 = self.cur_state['CLOSE'].values[1]
        reward = (v2 - v1) / v1

        if action == 0:
            return 0 - reward
        else:
            return reward

env = Env()

if __name__ == '__main__':
    env.get_state()
    print('')
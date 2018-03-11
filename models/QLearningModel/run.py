#encoding:utf-8
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(os.path.split(curPath)[0])[0]
sys.path.append(curPath)
sys.path.append(rootPath)

import pandas as pd
from models.QLearningModel.QLearningModel import QLearningModel
from models.QLearningModel.market import market
from models.base import plot_nav_curve
from models.config import config

class regression_test():

    def __init__(self, model, market):
        self.model = model
        self.market = market
        self.strategy_values = [1.0]
        self.market_values = [1.0]
        self.dates = [market.current_date.date()]
        self.train_episode = config.episode

    def train(self):
        market.stage = 'Train'
        for episode in range(self.train_episode):
            for i in range(len(market.train_pool)):
                obs, obs_ = market.get_state()
                action, _ = model.choose_action(obs)
                reward = market.get_reward(action)
                model.q_learn(obs, action, reward, obs_)

    def test(self, days):
        for i in range(days):
            print('\n[Current Date] ' + str(market.current_date.date()))
            market.stage = 'Test'
            model.epsilon = 1
            stocks = []
            for code in market.codes:
                obs, obs_ = market.get_state(code)
                if obs is None:
                    # print('Return None: ' + code)
                    continue
                action, pred_value = model.choose_action(obs)
                if action == '1':
                    act_reward = market.get_reward(action)
                    stocks.append([code, pred_value, act_reward])

            df = pd.DataFrame(stocks, columns=['CODE', 'PRDT_VALUE', 'ACT_REWARD'])
            tops = df.sort_values(ascending=False, by=['PRDT_VALUE']).head(5)

            avg_pred = tops['PRDT_VALUE'].mean()
            avg_act = tops['ACT_REWARD'].mean()

            # market_ratio = float(
            #     market.ratios[market.ratios['DATE'] == market.pass_days(market.current_date, 1)]['800_RATIO'])

            self.strategy_values.append(self.strategy_values[-1] * (1 + avg_act))
            # self.market_values.append(self.market_values[-1] * (1 + market_ratio / 100))
            self.market._pass_a_day()

            self.dates.append(market.current_date.date())
            # plot_nav_curve(self.strategy_values, self.market_values, self.dates)

            print('[Pred   ratio] ', avg_pred)
            print('[Act    ratio] ', avg_act)
            # print('[Market ratio] ', market_ratio)

    def load_model(self, path):
        model.load_model(path)

    def save_model(self, path):
        model.save_model(path)

if __name__ == '__main__':

    model = QLearningModel(learning_rate=0.1, gamma=0.0, e_greedy=0.9)
    reg_test = regression_test(model=model, market=market)

    # reg_test.train()
    # reg_test.save_model('/store/qlearning-model-new.csv')

    reg_test.load_model('/store/qlearning-model-new.csv')

    reg_test.test(days=30)
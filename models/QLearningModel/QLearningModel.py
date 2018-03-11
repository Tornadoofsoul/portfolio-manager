import pandas as pd
import numpy as np
from models.config import config

#learning_rate=0.1, gamma=0, e_greedy=1时候，最多迭代action次

class QLearningModel:
    def __init__(self, action_space=[0, 1], learning_rate=0.1, gamma=0.9, e_greedy=0.9):
        self.action_space = action_space
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = e_greedy
        self.q_table = pd.DataFrame(columns=self.action_space, dtype=np.float64)
        self.q_table_frequent = pd.DataFrame(columns=self.action_space, dtype=np.float64)

    def choose_action(self, state):

        self.check_state_exist(state)
        state_action = self.q_table.loc[state]

        if np.random.uniform() < self.epsilon:
            action = state_action.argmax()
        else:
            action = np.random.choice(self.action_space)
        value = state_action.loc[action]
        return action, value

    def q_learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.ix[s, a]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.ix[s_, :].max()
        else:
            q_target = r
        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)
        self.q_table_frequent.ix[s, a] += 1

    def sarsa_learn(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.ix[s, a]

        if s_ != 'terminal':
            state_action = self.q_table.ix[s, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))
            if np.random.uniform() < self.epsilon:
                a_ = state_action.argmax()
            else:
                a_ = np.random.choice(self.action_space)
            q_target = r + self.gamma * self.q_table.ix[s_, a_]
        else:
            q_target = r

        self.q_table.ix[s, a] += self.lr * (q_target - q_predict)
        self.q_table_frequent.ix[s, a] += 1

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series([0] * len(self.action_space), index=self.q_table.columns, name=state, ))
        if state not in self.q_table_frequent.index:
            self.q_table_frequent = self.q_table_frequent.append(
                pd.Series([0] * len(self.action_space), index=self.q_table_frequent.columns, name=state, ))

    def save_model(self, path):
        self.q_table.to_csv(config.rootPath + path)

    def load_model(self, path):
        self.q_table = pd.read_csv(config.rootPath + path, index_col=0)

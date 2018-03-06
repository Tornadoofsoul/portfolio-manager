#encoding:utf-8
from models.QLearningModel.QLearningModel import QLearningModel
from models.QLearningModel.env import env

if __name__ == '__main__':
    action_space = [0, 1]
    model = QLearningModel(action_space, learning_rate=0.1, gamma=0.0, e_greedy=0.9)

    for episode in range(2):
        for i in range(env.train.shape[0]):
            env.stage = 'Train'
            obs, obs_ = env.get_state()
            action = model.choose_action(obs)
            reward = env.get_reward(action)
            model.q_learn(obs, action, reward, obs_)
        print('Episode: ', episode)

    model.epsilon = 1

    for j in range(30):
        env.stage = 'Test'
        code = '000001.SZ'
        obs, obs_ = env.get_state(code)
        action = model.choose_action(obs)
        reward = env.get_reward(action)

        print('Reward:', reward, ', Action:', action)
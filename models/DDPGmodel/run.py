from task2.DDPGmodel import DDPGmodel
from task2.DQNmodel.env import env

train_window = 30
test_window = 10

env = env(train_window, test_window)
def ddpg_test():

    ddpg = DDPGmodel.DDPG(env)
    ddpg.fit()
    # ddpg.load_weights()
    ddpg.test()
    ddpg.save_weights()
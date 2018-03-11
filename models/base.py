#encoding:utf-8
import pandas as pd
from models.config import config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def make_diff(data_path):
    df = pd.read_csv(data_path, dtype={'CODE': 'str'})
    df['diff1'] = df.groupby(['CODE'])['CLOSE'].diff()
    df['diff2'] = df.groupby(['CODE'])['diff1'].diff()
    df.to_csv(data_path, index=False)

def plot_nav_curve(strategy_net_value, market_net_value, dates):
    plt.plot(dates, strategy_net_value, 'r-', label=strategy_net_value, linewidth=1.5)
    plt.plot(dates, market_net_value, 'g-', label=market_net_value, linewidth=1.5)

    plt.xlabel('Time')
    plt.ylabel('Net Asset Value')
    plt.legend(['strategy', 'market'], loc='upper left')
    plt.title("NAV")
    plt.grid(True)
    plt.xticks(fontsize=8, rotation=20)
    plt.ioff()
    plt.savefig(config.result)
    plt.close()

def gen_experience_display_pool(df):
    pool = []
    def apply(data):
        for i in range(data.shape[0] - 1):
            pool.append(data.iloc[i:i+2])

    df.groupby('CODE').apply(func=apply)
    return pool

if __name__ == '__main__':
    make_diff(config.ZZ800_DATA)
    print('')
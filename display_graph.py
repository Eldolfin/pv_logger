import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Shows the power production graph')
parser.add_argument('--average', help='Average the data over the given number of samples', type=int, default=0)

args = parser.parse_args()

ROLLING_WINDOW_SIZE = args.average

df = pd.read_csv('output.csv')

df['timestamp'] = pd.to_datetime(df['time'],unit='s')

if ROLLING_WINDOW_SIZE > 0:
    df['current_power'] = df['current_power'].rolling(window=ROLLING_WINDOW_SIZE).mean()

plt.plot()
sb.scatterplot(data=df, x='timestamp', y='current_power')
plt.show()

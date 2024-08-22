from static.orderbook.base_directory import file
import pandas as pd
from datetime import datetime

day_df = pd.read_csv(file)
day_df['timestamp'] = pd.to_datetime(day_df['entry_time'], format='%d-%m-%Y %H:%M')
day_df['date'] = day_df['timestamp'].dt.date
day_df['date'] = pd.to_datetime(day_df['date'])

# FOR SMA STRATEGY
sma_df = day_df[day_df['Metric'] == 'SMA']
if not sma_df.empty:
    day_on_day_sma = pd.DataFrame(columns=['Metric', 'total_wins', 'total_pnl', 'avg_pnl', 'win_percent', 'avg_pnl_win', 'avg_pnl_loss'])
    day_on_day_sma.loc[0, 'Metric'] = 'SMA'
    day_on_day_sma.loc[0, 'total_wins'] = sma_df[sma_df['pnl'] > 0].shape[0]
    day_on_day_sma.loc[0, 'total_pnl'] = round(sma_df['pnl'].sum(), 2)
    day_on_day_sma.loc[0, 'avg_pnl'] = round(day_on_day_sma.loc[0, 'total_pnl'] / sma_df.shape[0], 2)
    day_on_day_sma.loc[0, 'win_percent'] = round(day_on_day_sma.loc[0, 'total_wins'] * 100 / sma_df.shape[0], 2)
    day_on_day_sma.loc[0, 'avg_pnl_win'] = round(sma_df[sma_df['pnl'] > 0]['pnl'].mean(), 2)
    day_on_day_sma.loc[0, 'avg_pnl_loss'] = round(sma_df[sma_df['pnl'] < 0]['pnl'].mean(), 2)

# FOR SUPERTREND STRATEGY
supertrend_df = day_df[day_df['Metric'] == 'Supertrend']
if not supertrend_df.empty:
    day_on_day_supertrend = pd.DataFrame(columns=['Metric', 'total_wins', 'total_pnl', 'avg_pnl', 'win_percent', 'avg_pnl_win', 'avg_pnl_loss'])
    day_on_day_supertrend.loc[0, 'Metric'] = 'Supertrend'
    day_on_day_supertrend.loc[0, 'total_wins'] = supertrend_df[supertrend_df['pnl'] > 0].shape[0]
    day_on_day_supertrend.loc[0, 'total_pnl'] = round(supertrend_df['pnl'].sum(), 2)
    day_on_day_supertrend.loc[0, 'avg_pnl'] = round(day_on_day_supertrend.loc[0, 'total_pnl'] / supertrend_df.shape[0], 2)
    day_on_day_supertrend.loc[0, 'win_percent'] = round(day_on_day_supertrend.loc[0, 'total_wins'] * 100 / supertrend_df.shape[0], 2)
    day_on_day_supertrend.loc[0, 'avg_pnl_win'] = round(supertrend_df[supertrend_df['pnl'] > 0]['pnl'].mean(), 2)
    day_on_day_supertrend.loc[0, 'avg_pnl_loss'] = round(supertrend_df[supertrend_df['pnl'] < 0]['pnl'].mean(), 2)

final_df = pd.concat([day_on_day_sma, day_on_day_supertrend], ignore_index=True)
final_df.to_csv(r"static\orderbook\day_on_day_view\day_on_day_view.csv", index=False)
# print(sma_df.shape)
# print(supertrend_df.shape)
# print(day_on_day_sma.head())
# print(day_on_day_supertrend.head())
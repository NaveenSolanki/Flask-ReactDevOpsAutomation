from static.orderbook.base_directory import file
import pandas as pd
from datetime import datetime

month_df = pd.read_csv(file)
month_df['timestamp'] = pd.to_datetime(month_df['entry_time'], format='%d-%m-%Y %H:%M')
month_df['date'] = month_df['timestamp'].dt.date
month_df['date'] = pd.to_datetime(month_df['date'])

def filtered_dataframe(df):
    months_pnl = []
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    current_date = start_date
    
    while current_date < end_date:
        current_month = current_date.month
        current_year = current_date.year
        filtered_df = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
        
        if(filtered_df.empty):
            pnl = 0
        else:
            pnl = filtered_df['pnl'].sum()
        
        months_pnl.append(round(pnl,2))
        
        # Increment current_date by 1 month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)

    return pd.DataFrame({'pnl': months_pnl})



# FOR SMA STRATEGY 
sma_month_df = month_df[month_df['Metric'] == "SMA"]
sma_month_df = filtered_dataframe(sma_month_df)

month_on_month_sma = pd.DataFrame(columns=['Metric', 'total_wins', 'total_pnl', 'avg_pnl', 'win_percent', 'avg_pnl_win', 'avg_pnl_loss'])
month_on_month_sma.loc[0, 'Metric'] = 'SMA'
month_on_month_sma.loc[0, 'total_wins'] = sma_month_df[sma_month_df['pnl'] > 0].shape[0]
month_on_month_sma.loc[0, 'total_pnl'] = round(sma_month_df['pnl'].sum(), 2)
month_on_month_sma.loc[0, 'avg_pnl'] = round(sma_month_df['pnl'].mean(), 2)
month_on_month_sma.loc[0, 'win_percent'] = round(month_on_month_sma.loc[0, 'total_wins'] * 100 / sma_month_df.shape[0], 2)
month_on_month_sma.loc[0, 'avg_pnl_win'] = round(sma_month_df[sma_month_df['pnl'] > 0]['pnl'].mean(), 2)
month_on_month_sma.loc[0, 'avg_pnl_loss'] = round(sma_month_df[sma_month_df['pnl'] < 0]['pnl'].mean(), 2)

# FOR SUPERTREND STRATEGY
supertrend_month_df = month_df[month_df['Metric'] == "Supertrend"]
supertrend_month_df = filtered_dataframe(supertrend_month_df)

month_on_month_supertrend = pd.DataFrame(columns=['Metric', 'total_wins', 'total_pnl', 'avg_pnl', 'win_percent', 'avg_pnl_win', 'avg_pnl_loss'])
month_on_month_supertrend.loc[0, 'Metric'] = 'Supertrend'
month_on_month_supertrend.loc[0, 'total_wins'] = supertrend_month_df[supertrend_month_df['pnl'] > 0].shape[0]
month_on_month_supertrend.loc[0, 'total_pnl'] = round(supertrend_month_df['pnl'].sum(), 2)
month_on_month_supertrend.loc[0, 'avg_pnl'] = round(supertrend_month_df['pnl'].mean(), 2)
month_on_month_supertrend.loc[0, 'win_percent'] = round(month_on_month_supertrend.loc[0, 'total_wins'] * 100 / supertrend_month_df.shape[0], 2)
month_on_month_supertrend.loc[0, 'avg_pnl_win'] = round(supertrend_month_df[supertrend_month_df['pnl'] > 0]['pnl'].mean(), 2)
month_on_month_supertrend.loc[0, 'avg_pnl_loss'] = round(supertrend_month_df[supertrend_month_df['pnl'] < 0]['pnl'].mean(), 2)

final_df = pd.concat([month_on_month_sma, month_on_month_supertrend], ignore_index=True)
final_df.to_csv(r"static\orderbook\month_on_month_view\month_on_month_view.csv", index=False)
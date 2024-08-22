from static.orderbook.base_directory import file
import pandas as pd
from datetime import datetime

year_df = pd.read_csv(file)
year_df['timestamp'] = pd.to_datetime(year_df['entry_time'], format='%d-%m-%Y %H:%M')
year_df['date'] = year_df['timestamp'].dt.date
year_df['date'] = pd.to_datetime(year_df['date'])

def filtered_dataframe(df):
    years_pnl = []
    start_date = "2022-01-01"
    end_date = "2022-12-31"
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
    current_date = start_date
    
    while current_date < end_date:
        current_year = current_date.year
        filtered_df = df[df['date'].dt.year == current_year]
        
        if(filtered_df.empty):
            pnl = 0
        else:
            pnl = filtered_df['pnl'].sum()
        
        years_pnl.append(round(pnl,2))
        
        # Increment current_date by 1 year
        current_date = datetime(current_date.year + 1, 1, 1)
        
    return pd.DataFrame({'Year': range(start_date.year, end_date.year + 1), 'pnl': years_pnl})



# FOR SMA STRATEGY 
sma_year_df = year_df[year_df['Metric'] == "SMA"]
sma_year_df = filtered_dataframe(sma_year_df)

year_on_year_sma = pd.DataFrame(columns=['Metric', 'total_wins', 'total_pnl', 'avg_pnl', 'win_percent', 'avg_pnl_win', 'avg_pnl_loss'])
year_on_year_sma.loc[0, 'Metric'] = 'SMA'
year_on_year_sma.loc[0, 'total_wins'] = sma_year_df[sma_year_df['pnl'] > 0].shape[0]
year_on_year_sma.loc[0, 'total_pnl'] = round(sma_year_df['pnl'].sum(), 2)
year_on_year_sma.loc[0, 'avg_pnl'] = round(sma_year_df['pnl'].mean(), 2)
year_on_year_sma.loc[0, 'win_percent'] = round(year_on_year_sma.loc[0, 'total_wins'] * 100 / sma_year_df.shape[0], 2)
year_on_year_sma.loc[0, 'avg_pnl_win'] = round(sma_year_df[sma_year_df['pnl'] > 0]['pnl'].mean(), 2)
year_on_year_sma.loc[0, 'avg_pnl_loss'] = round(sma_year_df[sma_year_df['pnl'] < 0]['pnl'].mean(), 2)

# FOR SUPERTREND STRATEGY
supertrend_year_df = year_df[year_df['Metric'] == "Supertrend"]
supertrend_year_df = filtered_dataframe(supertrend_year_df)

year_on_year_supertrend = pd.DataFrame(columns=['Metric', 'total_wins', 'total_pnl', 'avg_pnl', 'win_percent', 'avg_pnl_win', 'avg_pnl_loss'])
year_on_year_supertrend.loc[0, 'Metric'] = 'Supertrend'
year_on_year_supertrend.loc[0, 'total_wins'] = supertrend_year_df[supertrend_year_df['pnl'] > 0].shape[0]
year_on_year_supertrend.loc[0, 'total_pnl'] = round(supertrend_year_df['pnl'].sum(), 2)
year_on_year_supertrend.loc[0, 'avg_pnl'] = round(supertrend_year_df['pnl'].mean(), 2)
year_on_year_supertrend.loc[0, 'win_percent'] = round(year_on_year_supertrend.loc[0, 'total_wins'] * 100 / supertrend_year_df.shape[0], 2)
year_on_year_supertrend.loc[0, 'avg_pnl_win'] = round(supertrend_year_df[supertrend_year_df['pnl'] > 0]['pnl'].mean(), 2)
year_on_year_supertrend.loc[0, 'avg_pnl_loss'] = round(supertrend_year_df[supertrend_year_df['pnl'] < 0]['pnl'].mean(), 2)

final_df = pd.concat([year_on_year_sma, year_on_year_supertrend], ignore_index=True)
final_df.to_csv(r"static\orderbook\year_on_year_view\year_on_year_view.csv", index=False)
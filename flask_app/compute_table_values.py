import pandas as pd
from datetime import datetime

class BaseClass():
    def __init__(self, file, start_date, end_date):
        self.file = file
        self.start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        self.end_date = pd.to_datetime(end_date, format='%Y-%m-%d')
        file['timestamp'] = pd.to_datetime(file['entry_time'], format='%d-%m-%Y %H:%M')
        file['date'] = file['timestamp'].dt.date
        file['date'] = pd.to_datetime(file['date'])
        

class DayOnDaySummary(BaseClass):
    def __init__(self, file, start_date, end_date):
        super().__init__(file, start_date, end_date)
        
    def total_wins(self, strategy):
        print(self.start_date)
        if strategy == 'SMA Option Buy': 
            tot_wnl = self.file[(self.file['date'] >= self.start_date) & (self.file['date'] <= self.end_date)]         
            options = tot_wnl[tot_wnl['pnl']>0].shape[0]
            
            return [0, options]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0]    

    def total_pnl(self, strategy):
        if strategy == 'SMA Option Buy':
            pnl = self.file[(self.file['date'] >= self.start_date) & (self.file['date'] <= self.end_date)]
            options = pnl['pnl'].sum()
            return [0,round(options,2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0,0]
    
    def average_pnl(self, strategy):
        if strategy == 'SMA Option Buy':
            avg_pnl = self.file[(self.file['date'] >= self.start_date) & (self.file['date'] <= self.end_date)]
            if not avg_pnl.empty:
                options = avg_pnl['pnl'].sum()
                avg = options/avg_pnl.shape[0]
                return [0, round(avg,2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0,0]    

    def win_percent(self, strategy):
        if strategy == 'SMA Option Buy':
            df = self.file[(self.file['date'] >= self.start_date) & (self.file['date'] <= self.end_date)]
            if not df.empty:
                profit = df[df['pnl']>0].shape[0]
                win_prct = profit*100/df.shape[0]
                return [0, round(win_prct,2)] 
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0]    

    def avg_pnl_win(self, strategy):
        if strategy == 'SMA Option Buy':
            df = self.file[(self.file['date'] >= self.start_date) & (self.file['date'] <= self.end_date)]
            profit = df[df['pnl']>0]
            if not profit.empty:
                total = profit.shape[0]
                profit = profit['pnl'].sum()
                return [0, round(profit/total,2)]  
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0]    

    def avg_pnl_loss(self, strategy):
        if strategy == 'SMA Option Buy':
            df = self.file[(self.file['date'] >= self.start_date) & (self.file['date'] <= self.end_date)]
            loss = df[df['pnl']<0]
            if not loss.empty:
                
                total = loss.shape[0]
                loss = loss['pnl'].sum()
                return [0, round(loss/total,2)]     
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0]    

class MonthOnMonthSummary(BaseClass):
    def __init__(self, file, start_date, end_date):
        super().__init__(file, start_date, end_date)
        months_pnl = []
        current_date = self.start_date
        if self.start_date == None:
            pass
        else:
            while current_date < self.end_date:
                current_month = current_date.month
                current_year = current_date.year
                filtered_df = self.file[(self.file['date'].dt.month == current_month) & (self.file['date'].dt.year == current_year)]
                
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
            print(months_pnl)
            self.months_df = pd.DataFrame({'pnl': months_pnl})
            print(self.months_df)
        
    def total_wins(self, strategy):
        if strategy == 'SMA Option Buy': 
            tot_wins = self.months_df[self.months_df['pnl'] > 0].shape[0]
            
            return [0, tot_wins]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def total_pnl(self, strategy):
        if strategy == 'SMA Option Buy':
            tot_pnl = self.months_df['pnl'].sum()
            return [0, round(tot_pnl,2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def average_pnl(self, strategy):
        if strategy == 'SMA Option Buy':
            avg_pnl = self.months_df['pnl'].sum()
            entries = self.months_df.shape[0]
            return [0, round(avg_pnl/entries,2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def win_percent(self, strategy):
        if strategy == 'SMA Option Buy':
            month_wins = self.months_df[self.months_df['pnl'] > 0].shape[0]
            tot_months = self.months_df.shape[0]
            percent = (month_wins*100)/tot_months
            return [0, round(percent, 2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0]  

    def avg_pnl_win(self, strategy):
        if strategy == 'SMA Option Buy':
            month_wins = self.months_df[self.months_df['pnl'] > 0]
            if month_wins.empty:
                return [0, 0]
            else:
                temp_df1 = month_wins['pnl'].sum()
                temp_df2 = month_wins.shape[0]
                return [0, round(temp_df1/temp_df2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def avg_pnl_loss(self, strategy):
        if strategy == 'SMA Option Buy':
            month_loss = self.months_df[self.months_df['pnl'] < 0]
            if month_loss.empty:
                return [0, 0]
            else:
                temp_df1 = month_loss['pnl'].sum()
                temp_df2 = month_loss.shape[0]
                return [0, round(temp_df1/temp_df2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

class YearOnYearSummary(BaseClass):
    def __init__(self, file, start_date, end_date):
        super().__init__(file, start_date, end_date)
        years_pnl = []
        current_date = self.start_date
        if self.start_date == None:
            pass
        else:
            while current_date < self.end_date:
                current_year = current_date.year
                filtered_df = self.file[self.file['date'].dt.year == current_year]
                
                if(filtered_df.empty):
                    pnl = 0
                else:
                    pnl = filtered_df['pnl'].sum()
                
                years_pnl.append(round(pnl,2))
                
                # Increment current_date by 1 year
                current_date = datetime(current_date.year + 1, 1, 1)
                
            self.years_df = pd.DataFrame({'Year': range(self.start_date.year, self.end_date.year + 1), 'pnl': years_pnl})
            
            
    def total_wins(self, strategy):
        if strategy == 'SMA Option Buy':
            tot_wins = self.years_df[self.years_df['pnl']>0].shape[0]
            return [0, tot_wins]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def total_pnl(self, strategy):
        if strategy == 'SMA Option Buy':
            tot_pnl = self.years_df['pnl'].sum()
            return [0, round(tot_pnl, 2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def average_pnl(self, strategy):
        if strategy == 'SMA Option Buy':
            avg_pnl = self.years_df['pnl'].sum()
            entries = self.years_df.shape[0]
            return [0, round(avg_pnl/entries,2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def win_percent(self, strategy):
        if strategy == 'SMA Option Buy':
            wins = self.years_df[self.years_df['pnl']>0].shape[0]
            entries = self.years_df.shape[0]
            percent = wins*100/entries
            return [0, round(percent, 2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def avg_pnl_win(self, strategy):
        if strategy == 'SMA Option Buy':
            year_wins = self.years_df[self.years_df['pnl'] > 0]
            if year_wins.empty:
                return [0, 0]
            else:
                temp_df1 = year_wins['pnl'].sum()
                temp_df2 = year_wins.shape[0]
                return [0, round(temp_df1/temp_df2, 2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

    def avg_pnl_loss(self, strategy):
        if strategy == 'SMA Option Buy':
            year_loss = self.years_df[self.years_df['pnl'] < 0]
            if year_loss.empty:
                return [0, 0]
            else:
                temp_df1 = year_loss['pnl'].sum()
                temp_df2 = year_loss.shape[0]
                return [0, round(temp_df1/temp_df2, 2)]
        # elif strategy == 'Supertrend Option Buy':
        return [0, 0] 

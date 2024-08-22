import io, boto3, os, pyodbc
from pymongo import MongoClient
import pandas as pd
from io import StringIO
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import  MediaIoBaseDownload

# Get the metric from website and return the calculation of that metric.
class Metric():
    def __init__(self, metric, source):
        self.metric = metric
        self.source = source
    
    def get_trading_strategy(self):
        set = 'sql'
        if set == 'local':
            file_dir = r"C:\Users\navee\OneDrive\Desktop\GitProject\GitProjectv1.4\flask_app\static\orderbook\local"
        
            # Read the three views
            day_on_day_view = pd.read_csv(os.path.join(file_dir, 'day_on_day_view.csv'))
            day_on_day_view.fillna(0, inplace=True)
            
            return day_on_day_view['Metric'].unique().tolist()
        else:
            COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQZpsZpk7jeupyhVg7qKbrmdaf897qfaI8uEsOC7qWOpI9CNpGTUCQcKQqxvLXq8fhJ52uLlwpACDbbIPeA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
            DATABASE_NAME = "performance_db"
            COLLECTION_NAME = "execution_table"

            # Establish a connection to the Cosmos DB
            client = MongoClient(COSMOS_CONNECTION_STRING)
            db = client[DATABASE_NAME]
            collection = db[COLLECTION_NAME]

            # Fetch all documents from the collection
            documents = collection.find()

            # Convert documents to a list of dictionaries
            data = [doc for doc in documents]

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(data)
            return df['strategy'].unique().tolist()
        
    # def get_values(self, day_df, month_df, year_df):
    #     day_view = {     
    #         "total_wins" : day_df['total_wins'].values[0],
    #         "total_pnl" : day_df['total_pnl'].values[0],
    #         "avg_pnl" : day_df['avg_pnl'].values[0],
    #         "win_percent" : day_df['win_percent'].values[0],
    #         "avg_pnl_win" : day_df['avg_pnl_win'].values[0],
    #         "avg_pnl_loss" : day_df['avg_pnl_loss'].values[0]   
    #     }
    #     month_view = {     
    #         "total_wins" : month_df['total_wins'].values[0],
    #         "total_pnl" : month_df['total_pnl'].values[0],
    #         "avg_pnl" : month_df['avg_pnl'].values[0],
    #         "win_percent" : month_df['win_percent'].values[0],
    #         "avg_pnl_win" : month_df['avg_pnl_win'].values[0],
    #         "avg_pnl_loss" : month_df['avg_pnl_loss'].values[0]    
    #     }
    #     year_view = {
    #         "total_wins" : year_df['total_wins'].values[0],
    #         "total_pnl" : year_df['total_pnl'].values[0],
    #         "avg_pnl" : year_df['avg_pnl'].values[0],
    #         "win_percent" : year_df['win_percent'].values[0],
    #         "avg_pnl_win" : year_df['avg_pnl_win'].values[0],
    #         "avg_pnl_loss" : year_df['avg_pnl_loss'].values[0]     
    #     }
    #     return {"day_view" : day_view, "month_view" : month_view, "year_view" : year_view}
    
    def get_values(self, day_df, month_df, year_df):
        def get_nested_view(df, job_type):
            filtered_df = df[df['job_type'] == job_type]
            if not filtered_df.empty:
                return {
                    "total_wins": filtered_df['total_wins'].values[0],
                    "total_losses": filtered_df['total_losses'].values[0],
                    "total_pnl": filtered_df['total_pnl'].values[0],
                    "avg_pnl": filtered_df['avg_pnl'].values[0],
                    "win_percent": filtered_df['win_percent'].values[0],
                    "avg_pnl_win": filtered_df['avg_pnl_win'].values[0],
                    "avg_pnl_loss": filtered_df['avg_pnl_loss'].values[0]
                }
            else:
                return {
                    "total_wins": 0,
                    "total_losses": 0,
                    "total_pnl": 0,
                    "avg_pnl": 0,
                    "win_percent": 0,
                    "avg_pnl_win": 0,
                    "avg_pnl_loss": 0
                }

        day_view = {
            "index_algo": get_nested_view(day_df, "index_algo"),
            "options_algo": get_nested_view(day_df, "options_algo")
        }

        month_view = {
            "index_algo": get_nested_view(month_df, "index_algo"),
            "options_algo": get_nested_view(month_df, "options_algo")
        }

        year_view = {
            "index_algo": get_nested_view(year_df, "index_algo"),
            "options_algo": get_nested_view(year_df, "options_algo")
        }

        return {"day_view": day_view, "month_view": month_view, "year_view": year_view}
        
    def sma(self, day_on_day_view, month_on_month_view, year_on_year_view):
        day_df = day_on_day_view[day_on_day_view['Metric'] == 'SMA'] 
        month_df = month_on_month_view[month_on_month_view['Metric'] == 'SMA'] 
        year_df = year_on_year_view[year_on_year_view['Metric'] == 'SMA'] 
        return self.get_values(day_df, month_df, year_df)
    
    def supertrend(self, day_on_day_view, month_on_month_view, year_on_year_view):
        day_df = day_on_day_view[day_on_day_view['Metric'] == 'Supertrend'] 
        month_df = month_on_month_view[month_on_month_view['Metric'] == 'Supertrend'] 
        year_df = year_on_year_view[year_on_year_view['Metric'] == 'Supertrend'] 
        return self.get_values(day_df, month_df, year_df)
             
    def custom_1(self, day_on_day_view, month_on_month_view, year_on_year_view):
        day_df = day_on_day_view[day_on_day_view['Metric'] == 'CUSTOM_1'] 
        month_df = month_on_month_view[month_on_month_view['Metric'] == 'CUSTOM_1'] 
        year_df = year_on_year_view[year_on_year_view['Metric'] == 'CUSTOM_1'] 
        return self.get_values(day_df, month_df, year_df)
    
    def rsi(self, day_on_day_view, month_on_month_view, year_on_year_view):
        day_df = day_on_day_view[day_on_day_view['Metric'] == 'RSI'] 
        month_df = month_on_month_view[month_on_month_view['Metric'] == 'RSI'] 
        year_df = year_on_year_view[year_on_year_view['Metric'] == 'RSI'] 
        return self.get_values(day_df, month_df, year_df)
    
    def local_fetching(self):
        file_dir = r"C:\Users\navee\OneDrive\Desktop\GitProject\GitProjectv1.4\flask_app\static\orderbook\local"
        
        # Read the three views
        day_on_day_view = pd.read_csv(os.path.join(file_dir, 'day_on_day_view.csv'))
        month_on_month_view = pd.read_csv(os.path.join(file_dir, 'month_on_month_view.csv'))
        year_on_year_view = pd.read_csv(os.path.join(file_dir, 'year_on_year_view.csv'))
        day_on_day_view.fillna(0, inplace=True)
        month_on_month_view.fillna(0, inplace=True)
        year_on_year_view.fillna(0, inplace=True)
        
        return day_on_day_view, month_on_month_view, year_on_year_view
        
    def fetch_csv_from_drive(self, service, folder_id, file_name):
        print(f"Fetching {file_name}...")
        file_query = f"name='{file_name}' and '{folder_id}' in parents"
        file_results = service.files().list(q=file_query).execute()
        file_id = file_results.get('files', [])[0]['id'] if file_results.get('files', []) else None
        
        if file_id:
            request = service.files().get_media(fileId=file_id)
            file_stream = io.BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()
            
            file_stream.seek(0)
            return pd.read_csv(file_stream, encoding='utf-8', header=0)
        else:
            print(f"File '{file_name}' not found.")
            return None

    def GDrive_fetching(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        token_json = r'C:\Users\navee\OneDrive\Desktop\GitProject\GitProjectv1.4\flask_app\token.json'
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
        drive_service = build('drive', 'v3', credentials=creds)

        folder_name = 'orderbook_views'
        day_file = 'day_on_day_view.csv'
        month_file = 'month_on_month_view.csv'
        year_file = 'year_on_year_view.csv'

        folder_query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        folder_results = drive_service.files().list(q=folder_query).execute()
        folder_id = folder_results.get('files', [])[0]['id'] if folder_results.get('files', []) else None

        if folder_id:
            day_df = self.fetch_csv_from_drive(drive_service, folder_id, day_file)
            month_df = self.fetch_csv_from_drive(drive_service, folder_id, month_file)
            year_df = self.fetch_csv_from_drive(drive_service, folder_id, year_file)
        else:
            print(f"Folder '{folder_name}' not found.")
            return None

        day_df.fillna(0, inplace=True)
        month_df.fillna(0, inplace=True)
        year_df.fillna(0, inplace=True)
                
        return day_df, month_df, year_df
    
    def S3_fetching(self):
        s3 = boto3.client('s3')
        bucket_name = 'algotradifyyearfetching'
        folder_name = 'orderbook_views'
        
        day_file = 'day_on_day_view.csv'
        month_file = 'month_on_month_view.csv'
        year_file = 'year_on_year_view.csv'
        
        # Construct the S3 object key
        day_s3_key = f"{folder_name}/{day_file}"
        month_s3_key = f"{folder_name}/{month_file}"
        year_s3_key = f"{folder_name}/{year_file}"
        
        try:
            # Get the CSV file object from S3
            day_obj = s3.get_object(Bucket=bucket_name, Key=day_s3_key)
            month_obj = s3.get_object(Bucket=bucket_name, Key=month_s3_key)
            year_obj = s3.get_object(Bucket=bucket_name, Key=year_s3_key)
            
            # Read the CSV file content
            day_csv_content = day_obj['Body'].read().decode('utf-8')
            month_csv_content = month_obj['Body'].read().decode('utf-8')
            year_csv_content = year_obj['Body'].read().decode('utf-8')
            
            # Convert CSV content to Pandas DataFrame
            day_df = pd.read_csv(StringIO(day_csv_content))
            month_df = pd.read_csv(StringIO(month_csv_content))
            year_df = pd.read_csv(StringIO(year_csv_content))
            
            day_df.fillna(0, inplace=True)
            month_df.fillna(0, inplace=True)
            year_df.fillna(0, inplace=True)
            
            return day_df, month_df, year_df
        except Exception as e:
            print(f"Error fetching file from S3: {str(e)}")
            return None
        
    def AzureSQL_fetching(self):
        # Define Azure SQL Database connection parameters
        server = 'algotradifyserver.database.windows.net'
        database = 'AlgoTradify'
        driver = '{ODBC Driver 18 for SQL Server}'
        username = 'admin'
        password = 'Algotrading'
        
        # Table names
        day_table = 'day_on_day_views'
        month_table = 'month_on_month_views'
        year_table = 'year_on_year_views'
        
        # Establish connection to Azure SQL Database
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        
        # SQL query to select all data from the Trades table
        day_query = f"SELECT * FROM {day_table}"
        month_query = f"SELECT * FROM {month_table}"
        year_query = f"SELECT * FROM {year_table}"

        # Execute the select query and fetch all rows
        day_df = pd.read_sql(day_query, conn)
        month_df = pd.read_sql(month_query, conn)
        year_df = pd.read_sql(year_query, conn)

        # Close the connection
        conn.close()
        
        return day_df, month_df, year_df
    
    def cosmos_mongoDB_fetching(self):
        COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
        DATABASE_NAME = "performance_db"
        COLLECTION_NAME_1 = "execution_table"
        COLLECTION_NAME_2 = "strategy_summary"

        # Establish a connection to the Cosmos DB
        client = MongoClient(COSMOS_CONNECTION_STRING)
        db = client[DATABASE_NAME]

        # Fetch all documents from the execution_table collection
        execution_table_collection = db[COLLECTION_NAME_1]
        execution_table_documents = execution_table_collection.find()
        execution_table_data = [doc for doc in execution_table_documents]
        execution_table = pd.DataFrame(execution_table_data)

        # Filter the execution_table DataFrame
        execution_table_filtered = execution_table[(execution_table['strategy'] == self.metric) & (execution_table['job_status'] == 'completed')]
        # execution_table_max_id = execution_table_filtered.iloc[-1]['ID']
        index_algo_df = execution_table_filtered[execution_table_filtered['job_type'] == 'index_algo']
        options_algo_df = execution_table_filtered[execution_table_filtered['job_type'] == 'options_algo']
        df1 = index_algo_df.sort_values(by='job_type', ascending=True)
        df2 = options_algo_df.sort_values(by='job_type', ascending=True)
        df1 = df1.iloc[-1:]
        df2 = df2.iloc[-1:]
        index_algo_max_id = df1.iloc[-1]['ID']
        options_algo_max_id = df2.iloc[-1]['ID']
        # Reset the cursor
        execution_table_documents.rewind()

        # Fetch only the required documents from the strategy_summary collection
        strategy_summary_collection = db[COLLECTION_NAME_2]
        strategy_summary_index_algo = strategy_summary_collection.find({'ID': int(index_algo_max_id)})
        strategy_summary_options_algo = strategy_summary_collection.find({'ID': int(options_algo_max_id)})

        # Convert fetched data to DataFrame
        strategy_summary_index_algo_df = pd.DataFrame(strategy_summary_index_algo)
        strategy_summary_options_algo_df = pd.DataFrame(strategy_summary_options_algo)

        # Rename columns
        strategy_summary_index_algo_df.rename(columns={'average_pnl': 'avg_pnl'}, inplace=True)
        strategy_summary_options_algo_df.rename(columns={'average_pnl': 'avg_pnl'}, inplace=True)

        # Additional columns
        strategy_summary_index_algo_df['Metric'] = self.metric
        strategy_summary_index_algo_df['job_type'] = 'index_algo'

        strategy_summary_options_algo_df['Metric'] = self.metric
        strategy_summary_options_algo_df['job_type'] = 'options_algo'

        # Concatenate DataFrames
        strategy_summary_filtered = pd.concat([strategy_summary_index_algo_df, strategy_summary_options_algo_df], ignore_index=True)

        # Filter views
        day_on_day_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'daily'].copy()
        month_on_month_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'monthly'].copy()
        year_on_year_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'yearly'].copy()

        # Fill NaN values
        day_on_day_view.fillna(0, inplace=True)
        month_on_month_view.fillna(0, inplace=True)
        year_on_year_view.fillna(0, inplace=True)

        return day_on_day_view, month_on_month_view, year_on_year_view
        
    def location(self):
        # Check the place from where we would fetch the ordebook data
        if self.source == 'local':
            return self.local_fetching()
        
        elif self.source == 'gdrive':
            return self.GDrive_fetching()
        
        elif self.source == 's3':
            return self.S3_fetching()
        
        elif self.source == 'sql':
            return self.cosmos_mongoDB_fetching()
            # return self.AzureSQL_fetching()
    
    def execute(self):
        # Fetch the data from the location selected in the webpage
        day_on_day_view, month_on_month_view, year_on_year_view = self.location()
        # Check what is the metric received from webpage
        if self.metric == 'SMA':
            return self.sma(day_on_day_view, month_on_month_view, year_on_year_view)
        elif self.metric == 'Supertrend':
            return self.supertrend(day_on_day_view, month_on_month_view, year_on_year_view)
        elif self.metric == 'CUSTOM_1':
            return self.custom_1(day_on_day_view, month_on_month_view, year_on_year_view)
        elif self.metric == 'RSI':
            return self.rsi(day_on_day_view, month_on_month_view, year_on_year_view)
                
        
# metric_results = Metric("SMA", 'sql').execute()
# # print(a.execute())
# table_data_day = [
#     {'': 'Total no. of win days', 'Index': metric_results['day_view']['index_algo']['total_wins'], 'Options': metric_results['day_view']['options_algo']['total_wins']},
#     {'': 'Total no. of loss days', 'Index': metric_results['day_view']['index_algo']['total_losses'], 'Options': metric_results['day_view']['options_algo']['total_losses']},
#     {'': 'Total PnL', 'Index': metric_results['day_view']['index_algo']['total_pnl'], 'Options': metric_results['day_view']['options_algo']['total_pnl']},
#     {'': 'Average PnL', 'Index': metric_results['day_view']['index_algo']['avg_pnl'], 'Options': metric_results['day_view']['options_algo']['avg_pnl']},
#     {'': 'Win Percent', 'Index': metric_results['day_view']['index_algo']['win_percent'], 'Options': metric_results['day_view']['options_algo']['win_percent']},
#     {'': 'Avg PnL win', 'Index': metric_results['day_view']['index_algo']['avg_pnl_win'], 'Options': metric_results['day_view']['options_algo']['avg_pnl_win']},
#     {'': 'Avg PnL loss', 'Index': metric_results['day_view']['index_algo']['avg_pnl_loss'], 'Options': metric_results['day_view']['options_algo']['avg_pnl_loss']},
# ]

# table_data_month = [
#     {'': 'Total no. of win months', 'Index': metric_results['month_view']['index_algo']['total_wins'], 'Options': metric_results['month_view']['options_algo']['total_wins']},
#     {'': 'Total no. of loss months', 'Index': metric_results['month_view']['index_algo']['total_losses'], 'Options': metric_results['month_view']['options_algo']['total_losses']},
#     {'': 'Total PnL', 'Index': metric_results['month_view']['index_algo']['total_pnl'], 'Options': metric_results['month_view']['options_algo']['total_pnl']},
#     {'': 'Average PnL', 'Index': metric_results['month_view']['index_algo']['avg_pnl'], 'Options': metric_results['month_view']['options_algo']['avg_pnl']},
#     {'': 'Win Percent', 'Index': metric_results['month_view']['index_algo']['win_percent'], 'Options': metric_results['month_view']['options_algo']['win_percent']},
#     {'': 'Avg PnL win', 'Index': metric_results['month_view']['index_algo']['avg_pnl_win'], 'Options': metric_results['month_view']['options_algo']['avg_pnl_win']},
#     {'': 'Avg PnL loss', 'Index': metric_results['month_view']['index_algo']['avg_pnl_loss'], 'Options': metric_results['month_view']['options_algo']['avg_pnl_loss']},
# ]

# table_data_year = [
#     {'': 'Total no. of win years', 'Index': metric_results['year_view']['index_algo']['total_wins'], 'Options': metric_results['year_view']['options_algo']['total_wins']},
#     {'': 'Total no. of loss years', 'Index': metric_results['year_view']['index_algo']['total_losses'], 'Options': metric_results['year_view']['options_algo']['total_losses']},
#     {'': 'Total PnL', 'Index': metric_results['year_view']['index_algo']['total_pnl'], 'Options': metric_results['year_view']['options_algo']['total_pnl']},
#     {'': 'Average PnL', 'Index': metric_results['year_view']['index_algo']['avg_pnl'], 'Options': metric_results['year_view']['options_algo']['avg_pnl']},
#     {'': 'Win Percent', 'Index': metric_results['year_view']['index_algo']['win_percent'], 'Options': metric_results['year_view']['options_algo']['win_percent']},
#     {'': 'Avg PnL win', 'Index': metric_results['year_view']['index_algo']['avg_pnl_win'], 'Options': metric_results['year_view']['options_algo']['avg_pnl_win']},
#     {'': 'Avg PnL loss', 'Index': metric_results['year_view']['index_algo']['avg_pnl_loss'], 'Options': metric_results['year_view']['options_algo']['avg_pnl_loss']},
# ]
# print(table_data_year)
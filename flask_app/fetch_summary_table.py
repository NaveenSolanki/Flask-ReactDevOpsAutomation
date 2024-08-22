from pymongo import MongoClient
import pandas as pd
import json
import numpy as np

class SummaryTable():
    def __init__(self, metric, source):
        self.metric = metric
        self.source = source
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
        trade_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'trade'].copy()
        day_on_day_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'daily'].copy()
        week_on_week_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'weekly'].copy()
        month_on_month_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'monthly'].copy()
        year_on_year_view = strategy_summary_filtered[strategy_summary_filtered['summary_level'] == 'yearly'].copy()

        
        # Fill NaN values
        trade_view.fillna(0, inplace=True)
        day_on_day_view.fillna(0, inplace=True)
        week_on_week_view.fillna(0, inplace=True)
        month_on_month_view.fillna(0, inplace=True)
        year_on_year_view.fillna(0, inplace=True)

        return trade_view, day_on_day_view, week_on_week_view, month_on_month_view, year_on_year_view
        
    def location(self):
        # Check the place from where we would fetch the ordebook data
        if self.source == 'sql':
            return self.cosmos_mongoDB_fetching()

class CompareSummaryTable():
    def __init__(self, metric_1, metric_2, metric_3, source, job_type):
        self.metric_1 = metric_1
        self.metric_2 = metric_2
        self.metric_3 = metric_3
        self.job_type = job_type
        self.source = source
    
    def cosmos_mongoDB_fetching(self):
        COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
        DATABASE_NAME = "performance_db"
        COLLECTION_NAME_1 = "execution_table"
        COLLECTION_NAME_2 = "strategy_summary"

        # Establish a connection to the Cosmos DB
        client = MongoClient(COSMOS_CONNECTION_STRING)
        db = client[DATABASE_NAME]

        # Initialize lists to store DataFrame views for each strategy
        strategy_views = []

        # Loop through each strategy
        for metric in [self.metric_1, self.metric_2, self.metric_3]:
            # Fetch all documents from the execution_table collection for the current strategy
            execution_table_collection = db[COLLECTION_NAME_1]
            execution_table_documents = execution_table_collection.find({'strategy': metric})
            execution_table_data = [doc for doc in execution_table_documents]
            execution_table_df = pd.DataFrame(execution_table_data)

            # Data Manipulation
            execution_table_filtered = execution_table_df[(execution_table_df['job_status'] == 'completed') & 
                                                        (execution_table_df['strategy'] == metric) & 
                                                        (execution_table_df['job_type'] == self.job_type)]
            algo_df = execution_table_filtered.sort_values(by='job_type', ascending=True).iloc[-1:]
            algo_max_id = algo_df.iloc[-1]['ID']

            # Fetch only the required documents from the strategy_summary collection for the current strategy
            strategy_summary_collection = db[COLLECTION_NAME_2]
            strategy_summary_data = strategy_summary_collection.find({'ID': int(algo_max_id)})
            strategy_summary_df = pd.DataFrame(strategy_summary_data)

            # Rename columns
            strategy_summary_df.rename(columns={'average_pnl': 'avg_pnl'}, inplace=True)

            # Additional columns
            strategy_summary_df['Metric'] = metric
            strategy_summary_df['job_type'] = self.job_type

            # Append the DataFrame view for the current strategy to the list
            strategy_views.append(strategy_summary_df)

        # Concatenate DataFrames for all strategies
        concatenated_df = pd.concat(strategy_views, ignore_index=True)

        # Filter views
        trade_view = concatenated_df[concatenated_df['summary_level'] == 'trade'].copy()
        day_on_day_view = concatenated_df[concatenated_df['summary_level'] == 'daily'].copy()
        week_on_week_view = concatenated_df[concatenated_df['summary_level'] == 'weekly'].copy()
        month_on_month_view = concatenated_df[concatenated_df['summary_level'] == 'monthly'].copy()
        year_on_year_view = concatenated_df[concatenated_df['summary_level'] == 'yearly'].copy()

        # Fill NaN values
        trade_view.fillna(0, inplace=True)
        day_on_day_view.fillna(0, inplace=True)
        month_on_month_view.fillna(0, inplace=True)
        year_on_year_view.fillna(0, inplace=True)
        week_on_week_view.fillna(0, inplace=True)

        return trade_view, day_on_day_view, week_on_week_view, month_on_month_view, year_on_year_view
    
    def location(self):
        # Check the place from where we would fetch the ordebook data
        if self.source == 'sql':
            return self.cosmos_mongoDB_fetching()

# print(CompareSummaryTable('CUSTOM_1', 'SMA', 'RSI', 'sql', 'options_algo').location())
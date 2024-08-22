import io, boto3, os, pyodbc
import pandas as pd
from flask import jsonify
from pymongo import MongoClient
from io import StringIO
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import  MediaIoBaseDownload

class ChartData():
    def __init__(self,source, metric):
        self.source = source
        self.metric = metric
    
    def local_fetching(self):
        file_dir = r"C:\Users\navee\OneDrive\Desktop\GitProject\GitProjectv1.4\flask_app\static\chart_csv"
        
        # Read the the chart data
        chart = pd.read_csv(os.path.join(file_dir, 'metric_for_chart.csv'))
        chart.fillna(0, inplace=True)
        # print(chart)
        return chart
    
    def GDrive_fetching(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        token_json = r'C:\Users\navee\OneDrive\Desktop\GitProject\GitProjectv1.4\flask_app\token.json'
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
        drive_service = build('drive', 'v3', credentials=creds)

        # Search for the folder within the parent folder
        folder_name = 'chart_csv'
        file_name = 'metric_for_chart.csv'
        folder_query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        folder_results = drive_service.files().list(q=folder_query).execute()
        folder_id = folder_results.get('files', [])[0]['id'] if folder_results.get('files', []) else None

        if folder_id:
            # Search for the specific file within the folder
            file_query = f"name='{file_name}' and '{folder_id}' in parents"
            file_results = drive_service.files().list(q=file_query).execute()
            file_id = file_results.get('files', [])[0]['id'] if file_results.get('files', []) else None
            if file_id:
                # Fetch the content of the file
                request = drive_service.files().get_media(fileId=file_id)
                file_stream = io.BytesIO()
                downloader = MediaIoBaseDownload(file_stream, request)

                # Download the file content
                done = False
                while not done:
                    status, done = downloader.next_chunk()

                # Reset the file stream cursor to the beginning
                file_stream.seek(0)
                return pd.read_csv(file_stream, encoding='utf-8', header=0)
            else:
                print(f"File '{file_name}' not found within '{folder_name}'.")
                return None
        else:
            print(f"Folder '{folder_name}' not found.")
    
    def S3_fetching(self):
        s3 = boto3.client('s3')
        bucket_name = 'algotradifyyearfetching'
        folder_name = 'chart_csv'
        
        chart_file = 'metric_for_chart.csv'
        
        # Construct the S3 object key
        s3_key = f"{folder_name}/{chart_file}"
        
        try:
            # Get the CSV file object from S3
            chart_obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
            
            # Read the CSV file content
            chart_csv_content = chart_obj['Body'].read().decode('utf-8')
            
            # Convert CSV content to Pandas DataFrame
            chart_df = pd.read_csv(StringIO(chart_csv_content))
            
            chart_df.fillna(0, inplace=True)
            
            return chart_df
        except Exception as e:
            print(f"Error fetching file from S3: {str(e)}")
            return None
        
    def AzureSQL_fetching(self):
        # Define Azure SQL Database connection parameters
        server = 'algotradifyserver.database.windows.net'
        database = 'AlgoTradify'
        driver = '{ODBC Driver 18 for SQL Server}'
        username = 'sqladmin'
        password = 'Algotradify@123'
        
        # Table name
        chart_table = 'chart_data'
        
        # Establish connection to Azure SQL Database
        conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        
        # SQL query to select all data from the chart table
        chart_query = f"SELECT * FROM {chart_table}"

        # Execute the select query and fetch all rows
        chart_df = pd.read_sql(chart_query, conn)

        # Close the connection
        conn.close()
        return chart_df
    
    def get_max_id_from_execution_table(self):
        COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
        DATABASE_NAME = "performance_db"
        COLLECTION_NAME = "execution_table"

        # Establish a connection to the Cosmos DB
        client = MongoClient(COSMOS_CONNECTION_STRING)
        db = client[DATABASE_NAME]

        # Fetch all documents from the execution_table collection
        execution_table_collection = db[COLLECTION_NAME]
        execution_table_documents = execution_table_collection.find()
        execution_table_data = [doc for doc in execution_table_documents]
        execution_table = pd.DataFrame(execution_table_data)

        # Filter the execution_table DataFrame
        execution_table_filtered = execution_table[(execution_table['strategy'] == self.metric) & (execution_table['job_status'] == 'completed') & (execution_table['job_type'] == 'index_algo')]
        execution_table_filtered = execution_table_filtered.sort_values(by = "ID", ascending=True)
        execution_table_max_id = execution_table_filtered.iloc[-1]['ID']
        return execution_table_max_id
    
    def cosmos_mongoDB_fetching(self):
        # Replace these with your Cosmos DB connection details
        COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
        DATABASE_NAME = "performance_db"
        COLLECTION_NAME = "chart_data_for_entry"

        # Establish a connection to the Cosmos DB
        client = MongoClient(COSMOS_CONNECTION_STRING)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        max_id = self.get_max_id_from_execution_table()
        documents = collection.find({'ID': int(max_id)})

        # Convert documents to a list of dictionaries
        data = [doc for doc in documents]
        
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(data)
        df.fillna(0, inplace=True)
        df.drop(columns='_id', inplace=True)
        df['Metric'] = self.metric
        return df
        
    def location(self):
        # Check the place from where we would fetch the chart data
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
        return self.location()
        # df = self.location()
        # return jsonify(df.to_dict(orient='records'))
             
# a = ChartData('sql', "CUSTOM_1")
# print(a.execute().head())
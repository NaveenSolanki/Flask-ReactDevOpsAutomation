from azure.cosmos import CosmosClient, PartitionKey
from static.CosmosDB.OptionParameters.cosmos_db_secret_key import cosmos_connection_string
import json, uuid
from pymongo import MongoClient
from datetime import datetime

def store_data_in_cosmos(json_data):
    # json_data = json.loads(json_string)
    json_data['id'] = str(uuid.uuid4())

    # Add current date and time
    json_data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Connect to Cosmos DB using the connection string
    client = MongoClient(cosmos_connection_string)

    # Select the database and collection
    database_name = 'performance_db'
    collection_name = 'option_parameters'

    # Get a reference to the database and collection
    db = client[database_name]
    collection = db[collection_name]

    # Insert the JSON data into the collection
    collection.insert_one(json_data)
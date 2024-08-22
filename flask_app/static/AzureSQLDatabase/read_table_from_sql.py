import pandas as pd
import pyodbc
from pymongo import MongoClient


def read_execution_record_sql_table():
    COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
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
    return df

def read_option_parameters_sql_table():
    COSMOS_CONNECTION_STRING = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"
    DATABASE_NAME = "performance_db"
    COLLECTION_NAME = "option_parameters"

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
    return df
# read_sql_table()
from pymongo import MongoClient
import pandas as pd

connection_string = "mongodb://mongodb-instance-cosmos-1:TMOLTJtQOMOSTZp903hlkajsfn7qKbrmI8uEsOC7qWOpI9aslfmboqihNLSAKlafkan390u0t332eA==@mongodb-instance-cosmos-1.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodb-instance-cosmos-1@"

# Close the connection
class MongoDBConnector:
    def __init__(self, database_name, connection_string=connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client.get_database(database_name)

    def write_dataframe_to_collection(self, collection_name, dataframe):
        if collection_name not in self.db.list_collection_names():
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        collection = self.db.get_collection(collection_name)
        data = dataframe.to_dict(orient='records')
        collection.insert_many(data)    
    
    # def write_dataframe_to_collection(self, collection_name, dataframe):
    #     collection = self.db.get_collection(collection_name)
    #     data = dataframe.to_dict(orient='records')
    #     collection.insert_many(data)
    
    def close_connection(self):
        self.client.close()

    # def create_collection(self, collection_name, shard_key=None):
    #     options = {}
    #     if shard_key:
    #         options['shardKey'] = shard_key
    #     self.db.create_collection(collection_name, **options)

    # def create_collection(self, collection_name, partition_key=None):
    #     options = {}
    #     if partition_key:
    #         options['partitionKey'] = partition_key
    #     self.db.create_collection(collection_name, **options)
    def create_collection(self, collection_name):
        self.db.create_collection(collection_name)

    def read_values_of_key(self, collection_name, key):
        if collection_name not in self.db.list_collection_names():
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        collection = self.db.get_collection(collection_name)
        documents = collection.find({}, {key: 1})
        values = [doc[key] for doc in documents]
        return values
    
    #create an update query with below logic and run it for a given table as argument
    #take key and value as arguments to filter for some rows
    #take an update key and updated value as arguments
    #for the filtered rows update key with respective value
    def update_rows_in_collection(self, collection_name, filter_key, filter_value, update_key, update_value):
        if collection_name not in self.db.list_collection_names():
            raise ValueError(f"Collection '{collection_name}' does not exist.")
        collection = self.db.get_collection(collection_name)
        filter_query = {filter_key: filter_value}
        update_query = {"$set": {update_key: update_value}}
        collection.update_many(filter_query, update_query)


# Example usage

if __name__ == "__main__":

    database_name = "performance_db"
    connector = MongoDBConnector(database_name)

    #connector.create_collection(collection_name="execution_table")
    #chart_data_for_entry
    #connector.create_collection(collection_name="chart_data_for_entry")
    connector.create_collection(collection_name="strategy_summary")
    # collection_name = "execution_table"
    # dataframe = pd.DataFrame({'run_id': [2,3], 'name': ['test_3','test_4']})

    # connector.write_dataframe_to_collection(collection_name, dataframe)

    # # Setup necessary steps to run query
    # # TODO: Add your code here

    connector.close_connection()



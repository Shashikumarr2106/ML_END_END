import pymongo
import pandas as pd
import json

data_file_path = "aps_failure_training_set1.csv"
database_name="aps"##
collection_name="sensor1"##table
MongoDB_URL="mongodb+srv://shashikumarr2106:8861250561@cluster0.tw9nr0b.mongodb.net/?retryWrites=true&w=majority"
mongo_client=pymongo.MongoClient(MongoDB_URL)
print(mongo_client)
df = pd.read_csv(data_file_path)

print(f"Rows and Columns:{df.shape}")

# convert dataframe to json format so that we can dump these records into mongo db
df.reset_index(drop=True,inplace=True)

json_record=list(json.loads(df.T.to_json()).values())
#print(json_record[0])

# insert converted json record to mongo db
mongo_client[database_name][collection_name].insert_many(json_record)
print("done......")

# Import some necessary modules
# pip install kafka-python
# pip install pymongo
# pip install "pymongo[srv]"
from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo.server_api import ServerApi

import json
uri = "mongodb+srv://admin:admin@cluster0.aas4upe.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

#try:
#    client.admin.command('ping')
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)

# Connect to MongoDB and pizza_data database

try:
    client = MongoClient(uri)
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    db = client.tkdapp
    print("MongoDB Connected successfully!")
except:
    print("Could not connect to MongoDB Aquiii")

consumer = KafkaConsumer('test',bootstrap_servers=[
    'my-kafka-0.my-kafka-headless.christianreyes11.svc.cluster.local:9092'
    ])
# Parse received data from Kafka
for msg in consumer:
    record = json.loads(msg.value)
    print(record)
    name = record['name']

    # Create dictionary and ingest data into MongoDB
    try:
       tkdapp_rec = {'name':name }
       print (tkdapp_rec)
       tkdapp_id = db.tkdapp_info.insert_one(tkdapp_rec)
       print("Data inserted with record ids", tkdapp_id)
    except:
       print("Could not insert into MongoDB")
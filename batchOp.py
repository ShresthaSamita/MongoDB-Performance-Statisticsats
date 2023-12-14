from pymongo import MongoClient
from faker import Faker

import csv
import certifi, time

fake = Faker()
execution_stats = []


def get_database():
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "USE_YOUR_MONGO_URL"
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['utsa-cloud-project-database']


# This is added so that many files can reuse the function get_database()


def operationFor(dataSize):
   # testing data
   # dataSize = 1000
   data = []
   for i in range(dataSize):
       item = {
           '_id': fake.uuid4(),
           'item_number': 150,
           'max_discount': fake.random_element(elements=('10%', '20%', '30%')),
           'batch_number': fake.unique.random_number(digits=10),
           'price': fake.random_int(min=10, max=1000),
           'category': fake.random_element(
               elements=('Kitchen appliance', 'Electronics', 'Clothing', 'Furniture', 'Food'))
       }
       data.append(item)


   # Insert the dummy data into a MongoDB collection
   db = get_database()
   collection = db["session"]


   # Insert each item and get execution stats for each operation
   start_time = time.time()
   collection.insert_many(data)
   insert_time = time.time() - start_time


   # perform update operation
   start_time = time.time()
   query = {"item_number": {"$gt": 100}}
   update = {"$set": {"max_discount": "55%"}}
   collection.update_many(query, update)
   update_time = time.time() - start_time


   # perform read operation
   start_time = time.time()
   docs = collection.find(query)
   read_time = time.time() - start_time


   # Perform delete operation
   start_time = time.time()
   query_result = collection.delete_many(query)
   delete_time = time.time() - start_time
   execution_stats.append({"dataSize": dataSize, "create" : insert_time, "read": read_time, "update" : update_time, "delete": delete_time })
   # Export execution stats to a CSV file
   filename = "/Users/samita/PycharmProjects/CloudProject/execution_statistics.csv"

multiple = 1000
round = 5

if __name__ == "__main__":
   # Get the database
   # dbname = get_database()
   for i in range(1, round+1):
       operationFor(i * multiple)
       time.sleep(60)
       print("round done!!")


# Export execution stats to a CSV file
filename = "/Users/samita/PycharmProjects/CloudProject/execution_statistics.csv"


# write the execution_stats list to a CSV file
with open(filename, mode='w') as csv_file:
   fieldnames = ['dataSize', 'create', 'read', 'update', 'delete', 'Execution Time']
   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)


   writer.writeheader()
   for stats in execution_stats:
       writer.writerow(stats)


print("Execution stats exported to execution_statistics.csv file")

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker

uri = "mongodb+srv://bookstoreAdmin:9QTngUHHhULpVK6V@cluster0.dm3qvxd.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

bookstoreDb = client['bookstore']
books = bookstoreDb['books']
print(books.find_one())
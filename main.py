from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI


uri = "mongodb+srv://bookstoreAdmin:9QTngUHHhULpVK6V@cluster0.dm3qvxd.mongodb.net/?retryWrites=true&w=majority"

app = FastAPI()

# Initialize MongoDB Client
client = AsyncIOMotorClient(uri)
bookstoreDb = client['bookstore']
books = bookstoreDb['books']

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


# print(books.find_one())


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/firstbook")
async def root():
    try:
        result = await books.find_one()
        return {"message": result["title"] + " by " + result["author"]}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}

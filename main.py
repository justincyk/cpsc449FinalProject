from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField
from bson import ObjectId


uri = "mongodb+srv://bookstoreAdmin:9QTngUHHhULpVK6V@cluster0.dm3qvxd.mongodb.net/?retryWrites=true&w=majority"

app = FastAPI()

# Initialize MongoDB Client
client = AsyncIOMotorClient(uri)
bookstoreDb = client['bookstore']
books = bookstoreDb['books']

# Book Model


class Book(BaseModel):
    id: ObjectIdField = None
    title: str
    author: str
    description: str
    price: float
    stock: int

    class Config:
        # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectId: str}


class BookRepository(AbstractRepository[Book]):
    class Meta:
        collection_name = 'books'


book_repository = BookRepository(database=books)


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
        # result = await book_repository.find_one_by({"author": "Jose Donoso"})
        # return result
        result = await books.find_one()
        return {"message": result["title"] + " by " + result["author"]}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}


@app.get("/books")
async def get_books():
    try:
        return {"message": "to do"}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}


@app.get("/books/{book_id}")
async def get_books_id():
    try:
        return {"message": "to do"}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}


@app.post("/books")
async def post_book():
    try:
        return {"message": "to do"}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}


@app.put("/books/{book_id}")
async def put_book():
    try:
        return {"message": "to do"}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}


@app.delete("/books/{book_id}")
async def delete_book():
    try:
        return {"message": "to do"}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}


@app.get("/search?title={}&author={}&min_price={}&max_price={}: ")
async def search_book():
    try:
        return {"message": "to do"}
    except DuplicateKeyError:
        return {"error": "Duplicate key error"}
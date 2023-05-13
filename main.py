from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError, PyMongoError
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField
from bson import ObjectId


uri = "mongodb+srv://bookstoreAdmin:9QTngUHHhULpVK6V@cluster0.dm3qvxd.mongodb.net/?retryWrites=true&w=majority"

app = FastAPI()

# Initialize MongoDB Client
client = AsyncIOMotorClient(uri)
bookstoreDb = client['bookstore']
booksCollection = bookstoreDb['books']

# Book Model
class Book(BaseModel):
    # id: ObjectIdField = None
    title: str
    author: str
    description: str
    price: float
    stock: int

    # class Config:
    #     # The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding
    #     json_encoders = {ObjectId: str}


# class BookRepository(AbstractRepository[Book]):
#     class Meta:
#         collection_name = 'books'


# book_repository = BookRepository(database=booksCollection)


# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)


# print(books.find_one())


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/firstbook")
# async def root():
#     try:
#         # result = await book_repository.find_one_by({"author": "Jose Donoso"})
#         # return result
#         result = await booksCollection.find_one()
#         return {"message": result["title"] + " by " + result["author"]}
#     except DuplicateKeyError:
#         return {"error": "Duplicate key error"}


@app.get("/books")
async def get_books():
    books = []
    for book in booksCollection.find({}):
        books.append(book)
    return books



@app.get("/books/{book_id}")
async def get_book(book_id: str):
    book = booksCollection.find_one({"_id": book_id})
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found!")



@app.post("/books")
async def add_book(book: Book):
    try:
        result = booksCollection.insert_one(book.dict())
        return {"id": str(result.inserted_id)}
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Error in adding book!")



@app.put("/books/{book_id}")
async def update_book(book_id: str, book: Book):
    try:
        result = booksCollection.update_one({"_id": book_id}, {"$set": book.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Book not found!")
        else:
            return {"message":"Book has been updated successfully!"}
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Error updating book!")



@app.delete("/books/{book_id}")
async def delete_book(book_id: str):
    try:
        result = booksCollection.delete_one({"_id": book_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found!")
        else:
            return {"message": "Book has been deleted successfully"}
    except PyMongoError:
        raise HTTPException(status_code=400, detail="Error in deleting book!")



@app.get("/search")
async def search_book(title: str = None, author: str = None, min_price: float = None, max_price: float = None):
    searchQuery = {}
    if title:
        searchQuery["title"] = title
    if author:
        searchQuery["author"] = author
    if min_price and max_price:
        searchQuery["price"] = {"$gte": min_price, "$lte": max_price}
    elif min_price:
        searchQuery["price"] = {"$gte": min_price}
    elif max_price:
        searchQuery["price"] = {"$lte": max_price}
    books = []
    for book in booksCollection.find(searchQuery):
        books.append(book)
    return books



# @app.get("/search?title={}&author={}&min_price={}&max_price={}")
# async def top():
#     total_books = booksCollection.count_documents({})
#     bestsellers = list(booksCollection.find().sort("stock", -1).limit(5))
#     top_authors = list(booksCollection.aggregate([
#         {"$group": {"_id": "$author", "count": {"$sum": 1}}},
#         {"$sort": {"count": -1}},
#         {"$limit": 5}
#     ]))
#     return {
#         "total_books": total_books,
#         "bestsellers": bestsellers,
#         "top_authors": top_authors
#     }

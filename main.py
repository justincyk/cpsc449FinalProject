import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio

URL = "mongodb+srv://bookstoreAdmin:9QTngUHHhULpVK6V@cluster0.dm3qvxd.mongodb.net/?retryWrites=true&w=majority"
app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(URL)
db = client.bookstore


# helper class to resolve ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# Book Model
class BookModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "The Obscene Bird of Night",
                "author": "José Donoso",
                "description": "A Chiliean Classic",
                "price": "16.00",
                "stock": "210",
            }
        }


class UpdatedBookModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "The Obscene Bird of Night",
                "author": "José Donoso",
                "description": "A Chiliean Classic",
                "price": "16.00",
                "stock": "210",
            }
        }


@app.get("/")
async def root():
    return {"message": "Welcome to the Book Store"}


@app.get("/books",
         response_description="Retrieve a list of all books in the store",
         response_model=List[BookModel])
async def list_books():
    books = await db["books2"].find().to_list(1000)
    return books


@app.get("/books/{id}",
         response_description="Retrieve a specific book by ID",
         response_model=BookModel)
async def find_book(id: str):
    if (book := await db["books2"].find_one({"_id": id})) is not None:
        return book
    else:
        raise HTTPException(status_code=404, detail=f"Book {id} not found")


@app.post("/books",
          response_description="Add a new book to the store",
          response_model=BookModel)
async def create_book(book: BookModel = Body(...)):
    book = jsonable_encoder(book)
    new_book = await db["books2"].insert_one(book)
    created_book = await db["books2"].find_one({"_id": new_book.inserted_id})
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_book)


@app.put("/books/{book_id}",
         response_description="Update an exisiting book by ID",
         response_model=BookModel)
async def update_book(id: str, book: UpdatedBookModel = Body(...)):
    book = {k: v for k, v in book.dict().items() if v is not None}
    if len(book) >= 1:
        updated_book = await db["books2"].update_one({"_id": id}, {"$set": book})
        if updated_book.modfied_count == 1:
            if (updated_book := await db["books2"].find_one({"_id": id})) is not None:
                return updated_book
    if (existing_book := await db["books2"].find_one({"_id": id})) is not None:
        return existing_book

    else:
        raise HTTPException(status_code=404, detail=f"Book {id} not found")


@app.delete("/books/{id}",
            response_description="Deletes a book from the store by ID")
async def delete_book(id: str):
    deleted_book = await db["books2"].delete_one({"_id": id})

    if deleted_book.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=404, detail=f"Book {id} not found")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Bookstore - CPSC 449",
        version="1.0.0",
        description="This is our OpenAPI schema for our bookstore",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

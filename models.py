import os
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional


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


def normalize(name: str) -> str:
    return ' '.join((word.capitalize()) for word in name.split(' '))


class BookModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    author: str = Field(...)
    description: str = Field(max_length=300)
    price: float = Field(
        gt=0, description="The price must be greater than zero")
    stock: int = Field(gt=0, description="The stock must be greater than zero")

    # validators
    @validator('author')
    def author_validator(cls, value):
        if ' ' not in value:
            raise ValueError('Author must contain first and last name')
        return value.title()

    _normalize_title = validator('title', allow_reuse=True)(normalize)
    _normalize_author = validator('author', allow_reuse=True)(normalize)
    _normalize_description = validator(
        'description', allow_reuse=True)(normalize)

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

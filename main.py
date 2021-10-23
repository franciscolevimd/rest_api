from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


books = [
    {'title': 'Lo que el viento se llevo', 'author_id': 2, 'genre_id': 2},
    {'title': 'La Iliada', 'author_id': 1, 'genre_id': 1},
    {'title': 'La Odisea', 'author_id': 1, 'genre_id': 1},
]


@app.get('/')
async def read_root():
    return {'Hello': 'Fack\'in Levi'}


@app.get('/books/')
async def read_book(skip: int = 0, limit: int = 10):
    return books[skip: skip + limit]


@app.get('/books/{resource_id}')
async def read_book_by_id(resource_id: int):
    return books[resource_id - 1]

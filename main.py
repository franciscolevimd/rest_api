from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Book(BaseModel):
    title: str
    author_id: int
    genre_id: int


books = []


@app.get('/')
async def read_root():
    return {'Hello': 'Fack\'in Levi'}


@app.get('/books/')
async def read_book(skip: int = 0, limit: int = 10):
    return books[skip: skip + limit]


@app.get('/books/{resource_id}')
async def read_book_by_id(resource_id: int):
    return books[resource_id - 1]


@app.post('/books/')
async def cretae_book(new_book: Book):
    books.append(new_book)
    return new_book


@app.put('/books/{resource_id}')
async def update_book(resource_id: int, modified_book: Book):
    book = books[resource_id - 1]
    books[resource_id - 1] = modified_book
    return book

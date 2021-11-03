import uvicorn
import secrets

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

from pydantic import BaseModel
from typing import Optional


app = FastAPI()
security = HTTPBasic()


class Book(BaseModel):
    book_id: Optional[int] = 0
    title: str
    author_id: int
    genre_id: int


books = []


def get_current_username(
        credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, 'levbono')
    correct_password = secrets.compare_digest(
        credentials.password, 'arisauriorex')
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'})
    return credentials.username


@app.get('/users/me')
def read_current_user(username: str = Depends(get_current_username)):
    return {'username': username}


@app.get('/')
async def read_root():
    return {'Hello': 'Fack\'in Levi'}


@app.get('/books/')
async def read_book(skip: int = 1, limit: int = 10):
    real_skip = get_real_skip(skip)
    return books[real_skip: real_skip + limit]


@app.get('/books/{book_id}')
async def read_book_by_id(book_id: int):
    book = find_book_by_id(book_id)
    if book is None:
        return {'Message': 'Book not found.'}
    return book


@app.post('/books/')
async def cretae_book(new_book: Book):
    new_book.book_id = get_new_book_id()
    books.append(new_book)
    return new_book


@app.put('/books/{book_id}')
async def update_book(book_id: int, modified_book: Book):
    book = find_book_by_id(book_id)
    if book is None:
        return {'Message': 'Book not found.'}
    book.title = modified_book.title
    book.author_id = modified_book.author_id
    book.genre_id = modified_book.genre_id
    return book


@app.delete('/books/{book_id}')
async def delete_book(book_id: int):
    real_id = get_real_id(book_id)
    if real_id < 0 or real_id >= len(books):
        return {'Message': 'Book not found.'}
    erased_book = books.pop(real_id)
    new_id = real_id
    for book in books:
        book.book_id = new_id
        new_id += 1
    return erased_book


def get_new_book_id():
    return len(books) + 1


def get_real_skip(skip: int):
    if skip < 1:
        return 0
    return skip - 1


def get_real_id(book_id: int):
    return book_id - 1


def find_book_by_id(book_id: int):
    real_id = get_real_id(book_id)
    if real_id < 0 or real_id >= len(books):
        return None
    return books[real_id]


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)

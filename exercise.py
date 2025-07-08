from fastapi import FastAPI, HTTPException,Body

from typing import *

app=FastAPI()

Books=[
    {'title':'Title one','author':'author one','category':'category one'},
    {'title':'Title two','author':'author one','category':'category two'},
    {'title':'Title three','author':'author three','category':'category three'},
    {'title':'Title four','author':'author four','category':'category four'},
    {'title':'Title 1','author':'author four','category':'category four'},
    {'title':'DeletionBook','author':'author four','category':'category four'},
]

@app.get('/')
def home():
    return {'message':'This is the first FastAPI porject of mine'}

@app.get('/items/{items_id}')
def rand(items_id:int):
    return {'message':f'the id is {items_id}'}

@app.get('/books')
async def books_read():
    return Books

@app.post('/books/add_book')
async def add_book(b=Body()):
    Books.append(b)

@app.put('/books/update_book')
async def update_book(book_details=Body()):
    for i in range(len(Books)):
        if Books[i].get('title').casefold()==book_details.get('title').casefold():
            Books[i]=book_details

#deletion using query parameter
@app.delete('/books/delete_book/')
async def delete_book(book_del:str):
    for i in range(len(Books)):
        if Books[i].get('title').casefold()==book_del.casefold():
            Books.pop(i)
            return f'{book_del} is deleted'
    return f"{book_del} doesn't exist"

#path parameter example
@app.get('/books/{book_req}')
async def req_book(book_req):
    for i in Books:
        if i.get('title').casefold()==book_req.casefold():
            return i
    return {'message':'Incorrect book id'}


#query parameter example
@app.get('/books/')
async def read_by_category(category:str):
    r=[]
    for i in Books:
        if i.get('category').casefold()==category.casefold():
            r.append(i)
    return r if len(r)>0 else 'incorrect category type'

#path parameter to fetch books of a specific author
@app.get('/books/author/')
async def fetch_by_Author(author_name:str):
    r=[]
    for i in range(len(Books)):
        if Books[i].get('author').casefold()==author_name.casefold():
            r.append(Books[i])
    return r if len(r)>0 else f'{author_name} has no books in the store'

@app.get('/books/{book_author}/')
async def read_by_auth_cate(book_author:str,category:str):
    r=[]
    for i in Books:
        if i.get('author').casefold()==book_author.casefold():
            if i.get('category').casefold()==category.casefold():
                r.append(i)
    return r if len(r)>0 else f'The {book_author} dont have any books in the {category}'


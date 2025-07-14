from fastapi import FastAPI,Body
from pydantic import BaseModel,Field
from typing import Annotated
app=FastAPI()

class Books(BaseModel):
    #id:Annotated[int,Field(ge=0,le=1000)]
    title:Annotated[str,Field(max_length=1000)] 
    author:Annotated[str,Field(max_length=1000)] 
    description:Annotated[str,Field(max_length=1000)]
    rating:Annotated[float,Field(ge=0,le=5)] 
    
class BookCreate(Books):
    id:int
        
books = [
    BookCreate(
        id=1,
        title="The Girl in the room 105",
        author="Chetan Bhagat",
        description="An exciting thriller with an unexpecting Ending, More like a detective novel",
        rating=5
    ),
    BookCreate(
        id=2,
        title= "One Indian Woman",
        author="Chetan Bhagat",
        description="Revolves around an introverted and intelligent Woman. and her relationships",
        rating=3.5
    ),
]

@app.get('/books')
async def get_books():
    return books

@app.post('/create-books')
async def create_books(new_book:Books):
    next_id=max([i.id for i in books]) + 1
    this_book=BookCreate(id=next_id,**new_book.model_dump())
    books.append(this_book)
    return "Book added succesfully"
    
    

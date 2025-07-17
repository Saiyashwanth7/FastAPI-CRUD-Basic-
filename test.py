from fastapi import FastAPI, Path, Query ,HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
import datetime


app = FastAPI()


class Books(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=100)]
    author: Annotated[str, Field(min_length=2, max_length=100)]
    description: Annotated[str, Field(min_length=2, max_length=100)]
    rating: Annotated[float, Field(ge=0, le=5)]
    published_year: Annotated[int, Field(ge=1770, le=2025)]


class Book_Id(Books):
    id: int


library = [
    Book_Id(
        id=1,
        title="Girl in Room 105",
        author="Chetan Bhagat",
        description="A suspenseful love story",
        rating=4.5,
        published_year=2018,
    ),
    Book_Id(
        id=2,
        title="Indian Woman",
        author="Chetan Bhagat",
        description="Explores the life of an Indian woman",
        rating=3.5,
        published_year=2020,
    ),
    Book_Id(
        id=3,
        title="The Alchemist",
        author="Paulo Coelho",
        description="A journey of following your dreams",
        rating=4.8,
        published_year=1988,
    ),
    Book_Id(
        id=4,
        title="To Kill a Mockingbird",
        author="Harper Lee",
        description="A novel about racial injustice",
        rating=4.9,
        published_year=1960,
    ),
    Book_Id(
        id=5,
        title="1984",
        author="George Orwell",
        description="A dystopian novel about totalitarianism",
        rating=4.7,
        published_year=1949,
    ),
    Book_Id(
        id=6,
        title="Pride and Prejudice",
        author="Jane Austen",
        description="A classic romance novel",
        rating=4.6,
        published_year=1813,
    ),
    Book_Id(
        id=7,
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        description="A critique of the American dream",
        rating=4.4,
        published_year=1925,
    ),
    Book_Id(
        id=8,
        title="Sapiens",
        author="Yuval Noah Harari",
        description="A brief history of humankind",
        rating=4.9,
        published_year=2011,
    ),
    Book_Id(
        id=9,
        title="Thinking, Fast and Slow",
        author="Daniel Kahneman",
        description="Insights into how we think",
        rating=4.8,
        published_year=2011,
    ),
    Book_Id(
        id=10,
        title="The Power of Habit",
        author="Charles Duhigg",
        description="How habits shape our lives",
        rating=4.5,
        published_year=2012,
    ),
]


@app.get("/books")
async def read_books():
    return library


@app.post("/books")
async def create_book(new_book: Books):
    if len(library) == 0:
        temp_id = 0
    else:
        temp_id = max([i.id for i in library])
    next_id = temp_id + 1
    library.append(Book_Id(id=next_id, **new_book.model_dump()))
    return f"{new_book.title} Book added succesfully!"


@app.get("/books/{book_id}")
async def book_by_id(book_id: int = Path(gt=0)):
    flag=False
    for book in library:
        if book.id == book_id:
            flag=True
            return {book}
    if not flag:
        raise HTTPException(status_code=404,detail='Book ID is invalid')
    


@app.get("/books/by-year")
async def read_by_year(year: int = Query(gt=1700, le=2025)):
    req_books = []
    for i in library:
        if i.published_year == year:
            req_books.append(i)
    return (
        req_books
        if len(req_books) > 0
        else {"message": f"Books of {year} are not available"}
    )


@app.get("/books/ratings/")
async def read_by_Rating(filter_rating: float = Query(ge=0, le=5)):
    req_books = []
    for book in library:
        if book.rating >= filter_rating:
            req_books.append(book)
    return req_books if len(req_books) > 0 else {"message": "Books not found"}


@app.put("/books")
async def update_book(updated_details: Books):
    flag=False
    for i in range(len(library)):
        if library[i].title.casefold() == updated_details.title.casefold():
            library[i] = Book_Id(id=library[i].id, **updated_details.model_dump())
            flag=True
    if not flag:
        raise HTTPException(status_code=404,detail="The Book doesn't exist")


@app.delete("/books/")
async def delete_book(book_id: int = Query(gt=0)):
    flag=False
    for i in range(len(library)):
        if library[i].id == book_id:
            library.pop(i)
            flag=True
    if not flag:
        raise HTTPException(status_code=404, detail="The Book ID is invalid")
    

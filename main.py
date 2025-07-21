from fastapi import FastAPI,Depends,Query,Path,HTTPException
from starlette import status
from database import sessionLocal,engine
import models
from models import Book
from typing import Annotated
from sqlalchemy.orm import session
from sqlalchemy import func
from pydantic import BaseModel,Field
app=FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
db_dependency=Annotated[session,Depends(get_db)]

class BookRequest(BaseModel):
    title:Annotated[str,Field(min_length=5)]
    author:Annotated[str,Field(min_length=2)]
    description:Annotated[str,Field(min_length=15)]
    rating:Annotated[int,Field(gt=0,le=5)]
    
@app.get('/',status_code=status.HTTP_200_OK)
async def read_db(db:db_dependency):
    return db.query(Book).all()

@app.get('/book/{author}',status_code=status.HTTP_200_OK)
async def read_by_author(db:db_dependency,author:str=Path(min_length=4)):
    book_item=db.query(Book).filter(func.lower(Book.author)==author.casefold()).all()
    if not book_item:
        raise HTTPException(status_code=404,detail='No books of this author')
    return book_item

@app.get('/book/by-id/',status_code=status.HTTP_200_OK)
async def read_by_id(db:db_dependency,book_id:int=Query(gt=0)):
    book_item=db.query(Book).filter(Book.id==book_id).first()
    if not book_item:
        raise HTTPException(status_code=404,detail='No books with this id')
    return book_item

@app.post('/book/upload/',status_code=status.HTTP_201_CREATED)
async def book_creation(db:db_dependency,book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    if not new_book:
        raise HTTPException(status_code=404,detail="Invalid field")
    db.add(new_book)
    db.commit()
    
@app.put('/book/update-book/{book_id}/',status_code=status.HTTP_204_NO_CONTENT)
async def update_book(db:db_dependency,book_request:BookRequest,book_id:int=Path(...,ge=1)):
    new_book=db.query(Book).filter(Book.id==book_id).first()
    if not new_book:
        raise HTTPException(status_code=404,detail='Invalid book details')
    new_book.title=book_request.title
    new_book.author=book_request.author
    new_book.description=book_request.description
    new_book.rating=book_request.rating
    
@app.delete('/book/delete/',status_code=status.HTTP_204_NO_CONTENT)
async def deletec_id(db:db_dependency,book_id:int=Query(gt=0)):
    book_request=db.query(Book).filter(Book.id==book_id).first()
    if not book_request:
        raise HTTPException(status_code=404,detail="The given id is invalid")
    db.delete(book_request)
    db.commit()
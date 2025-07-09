from fastapi import FastAPI,Body

app=FastAPI()

class Books:
    id:int
    title:str 
    author:str 
    description:str
    rating:int 
    
    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        
books = [
    Books(
        1,
        "The Girl in the room 105",
        "Chetan Bhagat",
        "An exciting thriller with an unexpecting Ending, More like a detective novel",
        5,
    ),
    Books(
        2,
        "One Indian Woman",
        "Chetan Bhagat",
        "Revolves around an introverted and intelligent Woman. and her relationships",
        3,
    ),
    Books(3, "Book1", "Author1", "Description", 3),
    Books(4, "Book4", "Author1", "Description", 2),
    Books(5, "Book7", "Author1", "Description", 2),
]

@app.get('/books')
async def get_books():
    return Books

@app.post('/create-books')
async def create_books(new_book=Body()):
    books.append(new_book)
    
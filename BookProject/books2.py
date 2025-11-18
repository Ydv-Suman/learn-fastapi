# Import necessary modules for FastAPI application
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

# Initialize FastAPI application instance
app = FastAPI()

# Book class: Represents a book entity with all its attributes
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    published_year: int

    # Constructor to initialize a Book object with all required fields
    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


# AddBook class: Pydantic model for validating book data when creating/updating books
#Includes constraints (min/max length, range checks, etc.)
class AddBook(BaseModel):
    id: Optional[int] = Field(description='Not required', default=None)
    title: str = Field(min_length=3, max_length=30)
    author: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=10, max_length=100)
    rating: float = Field(gt=-1, lt=6)
    published_year: int = Field(gt=1920, lt=2026)

    # Configuration for API documentation example
    model_config = {
        "json_schema_extra":{
            "example": {
                "title": "Title of a box",
                "author": "author of the box",
                "description": "Description of the book",
                "rating": 5,
                "published_year": 2020
            }
        }
    }

    
BOOKS = [
    Book(1, 'DBMS', 'Lon', 'Learn to handle data', 5, 2000),
    Book(2, 'OOP', 'Lon', 'Steps to be successful developer', 4.9, 2005),
    Book(3, 'Physics', 'Paul', 'elctricity and Magnetism', 4.5, 2012),
    Book(4, 'Network and Data Communication', 'Barnet', 'learn connectivity', 4.8, 1998),
    Book(5, 'Communication', 'Yajima', 'interpersonnel COmmunication', 4.4, 2015),
    Book(6, 'DSA', 'Lon', 'Data Structure and Algorithm', 5, 2010)
]

# GET endpoint: Retrieve all books from the collection
@app.get("/", status_code=status.HTTP_200_OK)
def getBooks():
    return BOOKS


# GET endpoint: Find a specific book by its ID
# Path parameter validation: book_id must be greater than 0
@app.get("/books/id/{book_id}", status_code=status.HTTP_200_OK)
def find_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"message": "no book found"}
    raise HTTPException( status_code=404, detail= "no book found")



# GET endpoint: Find books by their rating
# Query parameter: rating (float) - exact match required
@app.get("/books", status_code=status.HTTP_200_OK)
def read_Book_by_rating(rating: float):
    book_by_rating = []
    for book in BOOKS:
        if book.rating == rating:
            book_by_rating.append(book)
        if len(book_by_rating) == 0:
            return {"message": "No book found"}
    return book_by_rating


# POST endpoint: Create a new book
# Returns HTTP 201 (Created) status code on success
@app.post('/create_book', status_code=status.HTTP_201_CREATED)
def createBook(add_book: AddBook):
    new_book = Book(**add_book.dict())
    BOOKS.append(book_id(new_book))

# Helper function: Auto-generate book ID based on existing books
def book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


# PUT endpoint: Update an existing book
# Returns HTTP 204 (No Content) on successful update
@app.put("/books/update_books", status_code=status.HTTP_204_NO_CONTENT)
def updateBook(book: AddBook):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException( status_code=404, detail= "no book found")

# DELETE endpoint: Delete a book by its ID
# Returns HTTP 204 (No Content) on successful deletion
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteBook(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

# GET endpoint: Find books by their published year
# Query parameter validation: published_year must be between 1920 and 2025 (inclusive)
@app.get("/books/find_by_year", status_code=status.HTTP_200_OK)
def find_book_by_year(published_year: int = Query(gt=1919, lt=2026)):
    book_year = []
    for book in BOOKS:
        if book.published_year == published_year:
            book_year.append(book)
    if len(book_year) == 0:
        return {"message": "No books found for the given year"}
    return book_year
    raise HTTPException( status_code=404, detail= "no book found")
    
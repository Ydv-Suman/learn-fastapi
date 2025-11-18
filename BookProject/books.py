from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

## get request methods

@app.get("/")
async def first():
    return {"message": "Hello, World"}

@app.get("/books")
async def readBooks():
    return BOOKS


@app.get("/booksTitle/{book_title}")
async def readTitle(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_by_query(category: str):
    books = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books.append(book)
    return books

@app.get("/booksbyquery/{book_author}")
async def read_by_query2(book_author: str, category: str):
    books = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books.append(book)
    return books

## Post request method
@app.post("/books/createbooks")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

# PUT Request Method
@app.put("/books/updateBooks")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

# DELETE request method
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

# Practice
# Create a new API Endpoint that can fetch all books 
# from a specific author using either Path Parameters or Query Parameters.

@app.get("/books/book_by_author/{book_author}")
async def books_author(book_author : str):
    book_by_author = []
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == book_author.casefold():
            book_by_author.append(BOOKS[i])
    return book_by_author
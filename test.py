from dataclasses import dataclass

@dataclass
class Book:
    title : str

ba = Book("tralala")
print(ba)
ba.title = "fff"
print(ba)

def editBook(book, book_var, new_val):
    book_var.book_var = new_val

editBook(ba, ba.title, "ggg")
print(ba)
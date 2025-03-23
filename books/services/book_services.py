from books.models import Book

def create_book(data):
    return Book.objects.create(**data)

def update_book(book, data):
    for field, value in data.items():
        setattr(book, field, value)
    book.save()
    return book

def remove_book(book):
    book.delete()

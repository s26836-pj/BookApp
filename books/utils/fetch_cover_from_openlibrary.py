import requests


def fetch_cover_from_openlibrary(book):
    if not hasattr(book, 'isbn') or not book.isbn:
        print(f"No ISBN for: {book.title}")
        return

    cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
    response = requests.head(cover_url)

    if response.status_code == 200:
        book.cover_url = cover_url
        book.save()
        print(f"Updated cover from OpenLibrary: {book.title}")
    else:
        print(f"No cover in OpenLibrary for ISBN {book.isbn}")


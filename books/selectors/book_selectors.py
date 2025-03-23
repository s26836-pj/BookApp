from django.shortcuts import get_object_or_404

from books.models import Book


def get_books_by_filters(category_id=None, author=None, min_rating=None, max_rating=None):
    if category_id:
        return Book.objects.filter(category_id=category_id).order_by('id')

    if author:
        return Book.objects.filter(author_id=author).order_by('id')
    if min_rating:
        return Book.objects.filter(rating__gte=min_rating).order_by('id')
    if max_rating:
        return Book.objects.filter(rating__lte=max_rating).order_by('id')
    return Book.objects.all().order_by('id')


def get_book_by_id(book_id):
    return get_object_or_404(Book, id=book_id)


def get_all_books():
    return Book.objects.all().order_by('title')

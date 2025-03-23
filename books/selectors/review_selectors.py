from django.http import JsonResponse
from books.models import Review, Book


def get_reviews_for_book(book):
    return book.reviews.all().order_by("-id")


def get_review_by_id(review_id):
    return Review.objects.get(id=review_id)


def get_books_with_ratings():
    return [{"id": book.id, "average_rating": book.get_average_rating()} for book in Book.objects.all()]

from django.http import JsonResponse
from books.forms import ReviewForm
from books.models import Review
import logging

logger = logging.getLogger(__name__)


def create_review(user, book, data):
    try:
        review = Review.objects.create(
            user=user,
            book=book,
            content=data['content'],
            rating=data['rating']
        )
        return review, None
    except Exception as e:
        return None, str(e)


def delete_review(review):
    review.delete()

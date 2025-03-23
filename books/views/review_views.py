import logging
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from books.forms import ReviewForm
from books.models import Review, Book
from books.selectors.review_selectors import get_review_by_id, get_books_with_ratings
from books.services.review_services import create_review, delete_review
from books.utils.permissions import is_admin


@user_passes_test(is_admin)
@require_POST
def delete_review_view(request, review_id):
    review = get_review_by_id(review_id)
    book = review.book
    delete_review(review)

    new_avg_rating = book.get_average_rating() if book.reviews.exists() else 0

    return JsonResponse({
        "success": True,
        "review_id": review_id,
        "new_avg_rating": new_avg_rating
    })


logger = logging.getLogger(__name__)

def create_review_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if Review.objects.filter(user=request.user, book=book).exists():
        return JsonResponse({
            "success": False,
            "error": "You have already reviewed this book."
        })

    form = ReviewForm(request.POST, user=request.user, book=book)
    if form.is_valid():
        review, errors = create_review(request.user, book, form.cleaned_data)
        if review:
            rating = int(review.rating)
            return JsonResponse({
                "success": True,
                "review_id": review.id,
                "user": review.user.username,
                "content": review.content,
                "rating": rating,
                "new_avg_rating": book.get_average_rating()
            })
        else:
            return JsonResponse({"success": False, "error": errors})
    else:
        return JsonResponse({"success": False, "error": form.errors.get_json_data()})


def update_ratings(request):
    books_data = get_books_with_ratings()
    return JsonResponse({"books": books_data})

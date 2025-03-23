from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from books.models import Book
from books.selectors.review_selectors import get_reviews_for_book
from books.services.review_services import create_review

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews_list = get_reviews_for_book(book)
    paginator = Paginator(reviews_list, 5)
    page_number = request.GET.get("page")
    reviews = paginator.get_page(page_number)


    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        review, errors = create_review(request.user, book, request.POST)
        if review:
            new_avg_rating = book.get_average_rating()
            return JsonResponse({
                "success": True,
                "user": review.user.username,
                "content": review.content,
                "rating": review.rating,
                "new_avg_rating": new_avg_rating,
                "review_id": review.id,
                "total_pages": paginator.num_pages
            })
        else:
            return JsonResponse({"success": False, "error": errors})

    return render(request, 'book_app/book_detail.html', {
        'book': book,
        'reviews': reviews
    })
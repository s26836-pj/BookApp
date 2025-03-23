from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from books.models import Book, Category


def paginate_books(request, books, per_page=5):
    paginator = Paginator(books, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def home(request):
    books = Book.objects.all().order_by('id')
    categories = Category.objects.all()

    selected_category = request.GET.get("category")
    query = request.GET.get("q")

    if selected_category:
        selected_category = int(selected_category)
        books = books.filter(category_id=selected_category)

    if query:
        books = books.filter(title__icontains=query)

    for book in books:
        book.calculated_rating = book.get_average_rating()

    books_page = paginate_books(request, books)

    return render(request, "book_app/home.html", {
        "books": books_page,
        "categories": categories,
        "selected_category": selected_category,
        "request": request
    })


def filter_books_view(request):
    books = Book.objects.all().order_by('id')

    selected_category = request.GET.get("category")
    query = request.GET.get("q")

    if selected_category:
        selected_category = int(selected_category)
        books = books.filter(category_id=selected_category)

    if query:
        books = books.filter(title__icontains=query)

    books = books.annotate(calculated_rating=Avg("reviews__rating"))
    books_page = paginate_books(request, books)

    html = render_to_string("book_app/book_list.html", {
        "books": books_page,
        "selected_category": selected_category,
        "request": request
    })

    return JsonResponse({"html": html})

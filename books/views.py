from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReviewForm
from .models import Book, Category


def home(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        books = Book.objects.filter(category_id=category_id)
    else:
        books = Book.objects.all()

    return render(request, 'books/home.html', {
        'books': books,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(request, 'books/register.html', {'form': form})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            average_rating = book.average_rating

            return JsonResponse({
                "success": True,
                "user": request.user.username,
                "content": review.content,
                "rating": review.rating,
                "average_rating": average_rating
            })
        return JsonResponse({"success": False, "errors": form.errors})

    reviews = book.reviews.all()
    form = ReviewForm()

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': form,
        'average_rating': book.average_rating
    })
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from books.forms import BookForm, CategoryForm
from books.models import Category, Book
from books.selectors.book_selectors import get_all_books, get_book_by_id
from books.services.book_services import create_book, update_book, remove_book
from books.utils.fetch_cover_from_google_books import fetch_cover_from_google_books_local
from books.utils.fetch_cover_from_openlibrary import fetch_cover_from_openlibrary
from books.utils.permissions import is_admin
import os
from django.conf import settings


@user_passes_test(is_admin)
def manage_books(request):
    query = request.GET.get("q", "")
    books_list = get_all_books()

    if query:
        books_list = books_list.filter(title__icontains=query)

    paginator = Paginator(books_list, 5)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)

    return render(request, 'book_app/manage_books.html', {'books': books})


@user_passes_test(is_admin)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            create_book(form.cleaned_data)
            return redirect('manage_books')
    else:
        form = BookForm()
    return render(request, 'book_app/book_form.html', {'form': form, 'title': 'Add Book'})


@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_book_by_id(book_id)

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            update_book(book, form.cleaned_data)
            return redirect('manage_books')
    else:
        form = BookForm(initial={
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'category': book.category_id
        })

    return render(request, 'book_app/book_form.html', {
        'form': form,
        'title': 'Edit Book'
    })


@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_book_by_id(book_id)
    if request.method == "POST":
        remove_book(book)
        return redirect('manage_books')
    return render(request, 'book_app/book_confirm_delete.html', {'book': book})


@user_passes_test(is_admin)
def manage_categories(request):
    categories_list = Category.objects.all().order_by('name')
    paginator = Paginator(categories_list, 5)

    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)

    return render(request, 'book_app/manage_categories.html', {'categories': categories})


@user_passes_test(is_admin)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('manage_categories')
    return redirect('manage_categories')


@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    try:
        category.delete()
        messages.success(request, f"Category '{category.name}' deleted successfully.")
    except ProtectedError:
        messages.error(request, f"Cannot delete category '{category.name}' because it's assigned to existing books.")

    return redirect('manage_categories')


@user_passes_test(is_admin)
def fetch_all_covers(request):
    books = Book.objects.all()
    updated = 0

    for book in books:
        if not book.cover_url or book.cover_url.startswith("http"):
            fetch_cover_from_google_books_local(book)

            if not book.cover_url or book.cover_url.startswith("http"):
                fetch_cover_from_openlibrary(book)

            if book.cover_url and book.cover_url.startswith("/media/"):
                updated += 1

    messages.success(request, f"Updated covers for {updated} books.")
    return redirect("manage_books")


@user_passes_test(is_admin)
def fetch_cover_for_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    fetch_cover_from_google_books_local(book)

    if not book.cover_url or book.cover_url.startswith("http"):
        from books.utils.fetch_cover_from_openlibrary import fetch_cover_from_openlibrary
        fetch_cover_from_openlibrary(book)

    book.refresh_from_db()

    return redirect("home")


@user_passes_test(is_admin)
def reset_missing_covers(request):
    missing = 0
    books = Book.objects.exclude(cover_url__isnull=True).exclude(cover_url__exact='')

    for book in books:
        path = os.path.join(settings.BASE_DIR, book.cover_url.strip("/"))

        if not os.path.exists(path):
            book.cover_url = None
            book.save()
            missing += 1

        elif book.cover_url.startswith("/media/covers/"):
            try:
                os.remove(path)
                print(f"File deleted: {path}")
            except Exception as e:
                print(f"Could not be deleted: {path} ({e})")

            book.cover_url = None
            book.save()
            missing += 1

    messages.success(request, f"Removed {missing} covers.")
    return redirect("manage_books")

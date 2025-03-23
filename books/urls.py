from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from books.views import admin_views
from books.views.admin_views import manage_books, add_book, edit_book, delete_book, add_category, \
    delete_category, manage_categories, fetch_cover_for_book
from books.views.book_views import book_detail
from books.views.home_views import home, filter_books_view
from books.views.review_views import delete_review_view, update_ratings, create_review_view
from books.views.admin_views import fetch_all_covers

urlpatterns = [
                  path('', home, name='home'),
                  path('book/<int:book_id>/', book_detail, name='book_detail'),
                  path('manage/', manage_books, name='manage_books'),
                  path('manage/add/', add_book, name='add_book'),
                  path('manage/edit/<int:book_id>/', edit_book, name='edit_book'),
                  path('manage/delete/<int:book_id>/', delete_book, name='delete_book'),
                  path('categories/', manage_categories, name='manage_categories'),
                  path('categories/add/', add_category, name='add_category'),
                  path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),
                  path("update-ratings/", update_ratings, name="update_ratings"),
                  path('review/delete/<int:review_id>/', delete_review_view, name='delete_review'),
                  path('review/create/<int:book_id>/', create_review_view, name='create_review'),
                  path("filter-books/", filter_books_view, name="filter_books"),
                  path("admin/fetch-all-covers/", fetch_all_covers, name="fetch_all_covers"),
                  path("book/<int:book_id>/fetch-cover/", fetch_cover_for_book, name="fetch_cover_for_book"),
                  path("admin/reset-missing-covers/", admin_views.reset_missing_covers, name="reset_missing_covers"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

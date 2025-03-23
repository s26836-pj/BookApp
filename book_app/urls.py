
from django.urls import path, include
from django.contrib.auth import views

from books.views.auth_views import register

urlpatterns = [
    path('', include('books.urls')),
    path('login/', views.LoginView.as_view(template_name='book_app/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from books.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
    path('login/', views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]

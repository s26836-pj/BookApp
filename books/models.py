from django.db.models import PROTECT
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Properties
    @property
    def display_name(self):
        return self.name.upper() if self.name else ""

    #special method
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='books')
    cover_url = models.URLField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    #properties
    @property
    def short_description(self):
        return self.description[:77] + "..." if self.description and len(self.description) > 77 else self.description

    #Queries
    def get_average_rating(self):
        return self.reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"
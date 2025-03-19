from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    @property
    def display_name(self):
        return self.name.upper() if self.name else ""

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')

    @property
    def short_description(self):
        return self.description[:30] + "..." if self.description and len(self.description) > 30 else self.description

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        return round(sum(review.rating for review in reviews) / len(reviews), 1) if reviews else 0

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}/5)"
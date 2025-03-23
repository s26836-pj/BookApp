from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Review, Category


class ReviewForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.HiddenInput,
        error_messages={
            "required": "Rating is required.",
            "min_value": "Please provide a rating.",
            "max_value": "Maximum rating is 5 stars."
        }
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['content'].widget.attrs['placeholder'] = f"Your review, {self.user.username}"

    def clean(self):
        cleaned_data = super().clean()
        if self.user and self.book:
            if Review.objects.filter(user=self.user, book=self.book).exists():
                raise forms.ValidationError("You have already submitted a review for this book.")
        return cleaned_data


class BookForm(forms.Form):
    title = forms.CharField(max_length=255)
    author = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all())



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use another one.")
        return email

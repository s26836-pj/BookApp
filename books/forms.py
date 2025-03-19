from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} star") for i in range(1, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, label="Rating", widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['content'].widget.attrs['placeholder'] = f"Your review {user.username}"

    class Meta:
        model = Review
        fields = ["content", "rating"]

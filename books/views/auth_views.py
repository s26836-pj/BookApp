import logging
from django.contrib.auth import login
from django.shortcuts import redirect, render

from books.forms import CustomUserCreationForm


logger = logging.getLogger(__name__)


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            logger.error(f"Registration errors: {form.errors}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'book_app/register.html', {'form': form})


def register(request):
    return register_user(request)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from userprofile.models import UserProfile


def home(request):
    return render(request, 'home.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')

def plans(request):
    return render(request, 'plans.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()

            userprofile = UserProfile.objects.create(user=user)

            login(request, user)

            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form':form})

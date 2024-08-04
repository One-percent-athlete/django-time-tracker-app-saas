from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile

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

    return render(request, 'user/signup.html', {'form':form})

@login_required
def mypage(request):
    return render(request, 'user/mypage.html')

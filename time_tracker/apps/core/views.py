from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')

def plans(request):
    return render(request, 'plans.html')
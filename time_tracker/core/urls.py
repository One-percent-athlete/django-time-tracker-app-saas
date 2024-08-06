from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('plans/', views.plans, name='plans'),
]

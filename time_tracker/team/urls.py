from django.urls import path
from team import views

urlpatterns = [
    path('create/', views.create_team, name='create_team'),
]

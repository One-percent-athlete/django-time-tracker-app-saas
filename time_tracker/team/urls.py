from django.urls import path
from team import views

urlpatterns = [
    path('create/', views.create_team, name='create_team'),
    path('edit/', views.edit_team, name='edit_team'),
    path('invite/', views.invite, name='invite'),
    path('<int:team_id>/', views.team_detail, name='team_detail'),
    path('activate_team/<int:team_id>/', views.activate_team, name='activate_team'),
]

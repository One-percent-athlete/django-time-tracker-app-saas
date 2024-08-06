from django.urls import path
from userprofile import views

urlpatterns = [
    path('mypage/', views.mypage, name='mypage'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]

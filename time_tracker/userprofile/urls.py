from django.urls import path
from django.contrib.auth import views as auth_views
from userprofile import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('mypage/', views.mypage, name='mypage'),
]

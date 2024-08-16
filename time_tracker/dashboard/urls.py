from django.urls import path, include
from dashboard import views

urlpatterns = [  
    path('', views.dashboard, name='dashboard'),
    path('<int:user_id>/', views.show_user, name='show_user'),
    path('account/', include('userprofile.urls')),
    path('team/', include('team.urls')),
    path('project/', include('project.urls')),
]

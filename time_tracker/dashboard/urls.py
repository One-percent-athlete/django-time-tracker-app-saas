from django.urls import path, include
from dashboard import views

urlpatterns = [  
    path('', views.dashboard, name='dashboard'),
    path('account/', include('userprofile.urls')),
    path('team/', include('team.urls')),
    path('project/', include('project.urls')),
]

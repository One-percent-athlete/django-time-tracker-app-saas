from django.urls import path
from project import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/<int:task_id>/', views.task, name='task'),
    path('<int:project_id>/<int:task_id>/edit/', views.edit_task, name='edit_task'),
]

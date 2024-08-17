from django.urls import path
from project import views, api

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<int:project_id>/', views.project, name='project'),
    path('<int:project_id>/edit/', views.edit_project, name='edit_project'),
    path('<int:project_id>/<int:task_id>/', views.task, name='task'),
    path('<int:project_id>/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('<int:project_id>/<int:task_id>/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('<int:project_id>/<int:task_id>/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),

    path('api/start_timer/', api.api_start_timer, name='api_start_timer'),
    path('api/stop_timer/', api.api_stop_timer, name='api_stop_timer'),
    path('api/discard_timer/', api.api_discard_timer, name='api_discard_timer')
]

from django.db import models

from django.contrib.auth.models import User

from team.models import Team

class Project(models.Model):
    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name='projects', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.created_by}"
    
    def registered_at(self):
        return 0
    
    def num_tasks_todo(self):
        return 0
    
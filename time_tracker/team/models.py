from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    INACTIVE = 'inactive'
    ACTIVE = 'active'
    DELETED = 'deleted'

    CHOICES_STATUS = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=CHOICES_STATUS, default=INACTIVE)

    class Meta:
        ordering = ['name', 'created_at']
    
    def __str__(self):
        return f"{self.id} - {self.name}"
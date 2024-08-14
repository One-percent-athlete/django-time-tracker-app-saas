from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    ACTIVE = 'active'
    DELETED = 'deleted'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='teams')
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=CHOICES_STATUS, default=ACTIVE)

    class Meta:
        ordering = ['name', 'created_at']
    
    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Invite(models.Model):
    INVITED = 'invited'
    ACCEPTED = 'accepted'

    CHOICES_STATUS = (
        (INVITED, 'Invited'),
        (ACCEPTED, 'Accepted')
    )

    team = models.ForeignKey(Team, related_name='invite', on_delete=models.CASCADE)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=INVITED)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.status} - {self.date_sent}" 
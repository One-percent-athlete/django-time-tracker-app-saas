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
    
    def registered_time(self):
        # time = 0

        # entries = self.entries.all()

        # for entry in entries:
        #     time = time + entries.minutes

        # return time

        return sum(entry.minutes for entry in self.entries.all())
    
    def num_tasks_todo(self):
        return self.tasks.filter(status=Task.TODO).count()
    
class Task(models.Model):

    TODO = 'todo'
    DONE = 'done'
    ARCHIVED = 'archived'

    CHOICES_STATUS = (
        (TODO, 'Todo'),
        (DONE, 'Done'),
        (ARCHIVED, 'Archived'),
    )


    name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, related_name='tasks', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=TODO)

    class Meta:
       ordering = ['-created_at']

    def __str__(self):
        return self.name 
    
    def registered_time(self):
        return sum(entry.minutes for entry in self.entries.all())

class Entry(models.Model):
    team = models.ForeignKey(Team, related_name='entries', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey(Task, related_name='entries', on_delete=models.CASCADE, blank=True, null=True)
    minutes = models.IntegerField(default=0)
    is_tracked = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='entries', on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
       ordering = ['-created_at']
       verbose_name_plural = "entries"


    def __str__(self):
        if self.task:
            return '%s - %s' % (self.task.name, self.created_at)
        return '%s' % self.created_at
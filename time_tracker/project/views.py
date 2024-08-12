from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Project, Task, Entry
from team.models import Team

@login_required
def projects(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = Project.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            project = Project.objects.create(team=team, name=name, created_by=request.user)

            messages.info(request, 'The Project Is Added.')

            return redirect('projects')

    return render(request, 'project/projects.html', {'team': team, 'projects': projects})

@login_required
def project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            task = Task.objects.create(team=team, project=project, name=name, created_by=request.user)

            messages.info(request, 'The Task Is Added.')

            return redirect('project', project_id=project.id)
        
    tasks_todo = project.tasks.filter(status=Task.TODO)
    tasks_done = project.tasks.filter(status=Task.DONE)

    return render(request, 'project/project.html', {'team':team, 'project':project, 'tasks_todo':tasks_todo, 'tasks_done':tasks_done})

@login_required
def edit_project(request, project_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)

    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            project.name = name
            project.save()

            messages.info(request, 'The Project Is Updated.')

            return redirect('project', project_id=project.id)



    return render(request, 'project/edit_project.html', {'team':team, 'project':project})

@login_required
def task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())
        minutes_total = (hours * 60) + minutes

        entry = Entry.objects.create(team=team, project=project, task=task, minutes=minutes_total, created_by=request.user, created_at=date)
        return redirect('project', project_id=project.id)
    return render(request, 'project/task.html', {'team':team, 'project':project, 'task':task, 'today': datetime.today()})

@login_required
def edit_task(request, project_id, task_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)

    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')

        if name:
            task.name = name
            task.status = status
            task.save()

            messages.info(request, 'The Task Is Updated.')

            return redirect('task', project_id=project.id, task_id=task.id)



    return render(request, 'project/edit_task.html', {'team':team, 'project':project, 'task':task})

@login_required
def edit_entry(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)

    if request.method == 'POST':
        hours = int(request.POST.get('hours', 0))
        minutes = int(request.POST.get('minutes', 0))
        date = '%s %s' % (request.POST.get('date'), datetime.now().time())

        entry.created_at = date
        entry.minutes = (hours * 60) + minutes
        entry.save()

        messages.info(request, 'The Entry Is Updated.')

        return redirect('task', project_id=project.id, task_id=task.id)
    
    hours, minutes = divmod(entry.minutes, 60)

    return render(request, 'project/edit_entry.html', {'team':team, 'project':project, 'task':task, 'entry': entry, 'hours': hours, 'minutes':minutes})

@login_required
def delete_entry(request, project_id, task_id, entry_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    project = get_object_or_404(Project, team=team, pk=project_id)
    task = get_object_or_404(Task, pk=task_id, team=team)
    entry = get_object_or_404(Entry, pk=entry_id, team=team)

    entry.delete()

    messages.info(request, 'The Entry Is Deleted.')

    return redirect('task', project_id=project.id, task_id=task.id)


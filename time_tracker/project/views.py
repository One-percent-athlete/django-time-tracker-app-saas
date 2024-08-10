from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Project
from team.models import Team

@login_required
def projects(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = Project.objects.all()

    return render(request, 'project/projects.html', {'team': team, 'projects': projects})

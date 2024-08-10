from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Team
from userprofile.models import UserProfile

@login_required
def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            team = Team.objects.create(name=name, created_by=request.user)
            team.memebers.add(request.user)
            team.save()

            userprofile = UserProfile.objects.get(user=request.user.id)
            userprofile.active_team_id = team.id
            userprofile.save()
            return redirect('mypage')
    return render(request, 'team/create_team.html')
# def active_team(request):
#     if request.user.is_authenticated:
#         if request.user.userprofile.active_team_id:
#             active_team = Team.objects.get(pk=request.user.userprofile.active_team_id)

#             return {'active_team': active_team}
#     return {'active_team': None }

@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])

    return render(request, 'team/team_detail.html', {'team': team})

@login_required
def edit_team(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE, members__in=[request.user])

    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            team.name = name
            team.save()

            messages.info(request, 'Change Saved Successfully.')

            return redirect('team_detail', team_id = team.id)

    return render(request, 'team/edit_team.html', {'team': team})

@login_required
def activate_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id, status=Team.ACTIVE, members__in=[request.user])
    userprofile = request.user.userprofile
    userprofile.active_team_id = team.id
    userprofile.save()

    messages.info(request, 'The Team Was Activated.')
    return redirect('mypage')
    
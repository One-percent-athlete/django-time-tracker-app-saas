from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random

from .models import Team, Invitation
from userprofile.models import UserProfile
from .utilities import send_invitation, invitation_accepted

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
    invitations = team.invitations.filter(status=Invitation.INVITED)

    return render(request, 'team/team_detail.html', {'team': team, 'invitations':invitations})

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
    

@login_required
def invite(request):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:
            invitations = Invitation.objects.filter(team=team, email=email)

            if not invitations:
                code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(4))
                invitation = Invitation.objects.create(team=team, email=email, code=code)

                messages.info(request, 'Invitation Sent.')

                send_invitation(email, code, team)
                return redirect('team', team_id=team.id)
            else:
                messages.info(request, 'The User Has Already Been Invited.')
                return
    return render(request, 'team/invite.html', {'team': team})


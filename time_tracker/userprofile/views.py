from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from team.models import Team

@login_required
def mypage(request):
    teams = Team.objects.exclude(pk=request.user.userprofile.active_team_id)
    if request.user.userprofile.active_team_id:
        active_team = Team.objects.get(pk=request.user.userprofile.active_team_id)
    return render(request, 'user/mypage.html', {'teams':teams, 'active_team': active_team})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        messages.success(request, 'Your Profile Has Been Updated.')
        return redirect('mypage')

    return render(request, 'user/edit_profile.html')
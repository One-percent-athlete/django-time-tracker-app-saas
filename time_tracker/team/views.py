from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .models import Team

@login_required
def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            team = Team.objects.create(name=name, created_by=request.user)
            team.memebers.add(request.user)
            team.save()

            userprofile = request.user.userprofile
            userprofile.active_team_id = team.id
            userprofile.save()
            return redirect('mypage')
    return render(request, 'team/create_team.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from team.models import Team, Invitation
from team.utilities import invitation_accepted


@login_required
def mypage(request):
    teams = Team.objects.exclude(pk=request.user.userprofile.active_team_id)
    invitations = Invitation.objects.filter(email=request.user.email, status=Invitation.INVITED)

    return render(request, 'user/mypage.html', {'teams':teams, 'invitations':invitations})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        if request.FILES:
            avatar = request.FILES['avatar']
            userprofile = request.user.userprofile
            userprofile.avatar = avatar
            userprofile.save()

        messages.success(request, 'Your Profile Has Been Updated.')
        return redirect('mypage')

    return render(request, 'user/edit_profile.html')

@login_required
def accept_invitation(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.user.email
        invitations = Invitation.objects.filter(code=code, email=email)

        if invitations:
            invitation = invitations[0]
            invitation.status = Invitation.ACCEPTED
            invitation.save()

            team = invitation.team
            team.members.add(request.user)
            team.save()

            userporfile = request.user.userprofile
            userporfile.active_team_id = team.id
            userporfile.save()

            messages.info(request, 'Invitation Accepted.')

            invitation_accepted(email, team, invitation)

            return redirect('team', team_id=team.id)
        else:
            messages.info(request, 'Invitation Not Found.')
            return redirect('mypage')
    else:
        return render(request, 'user/accept_invitation.html')

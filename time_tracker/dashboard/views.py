from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from project.models import Entry
from team.models import Team
from dashboard.utilities import *


@login_required
def dashboard(request):
    if not request.user.userprofile.active_team_id:
        return redirect('mypage')
    
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.all()
    members = team.members.all()

    num_days = int(request.GET.get('num_days', 0))
    user_date = datetime.now() - timedelta(days=num_days)
    entries = Entry.objects.filter(team=team, created_by=request.user, created_at__date=user_date, is_tracked=True)


    user_num_months = int(request.GET.get('num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)
    for project in projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, project, request.user, user_month)


    team_num_months = int(request.GET.get('team_num_months', 0))
    team_month = datetime.now() - relativedelta(months=team_num_months)

    for member in members:
        member.time_for_user_and_team_and_month = get_time_for_user_and_team_and_month(team, member, team_month)

    
    untracked_entries = Entry.objects.filter(team=team, created_by=request.user, is_tracked=False).order_by('-created_at')

    for untracked_entry in untracked_entries:
        untracked_entry.minutes_since = int((datetime.now(timezone.utc) - untracked_entry.created_at).total_seconds() / 60)


    context = {
        'team': team,
        'members': members,
        'projects':projects,
        'latest_projects':projects[0:4],
        
        'entries': entries,
        'untracked_entries':untracked_entries,


        'num_days': num_days,
        'user_date':user_date,

        'user_num_months': user_num_months,
        'user_month': user_month,

        'team_num_months':team_num_months,
        'team_month':team_month,

        'time_for_user_and_month': get_time_for_user_and_month(team, request.user, user_month),
        'time_for_user_and_date': get_time_for_user_and_date(team, request.user, user_date),
        'time_for_team_and_month': get_time_for_team_and_month(team, team_month)
    }


    return render(request, 'dashboard/dashboard.html', context)

@login_required
def show_user(request, user_id):
    team = get_object_or_404(Team, pk=request.user.userprofile.active_team_id, status=Team.ACTIVE)
    projects = team.projects.all()
    user = team.members.all().get(id=user_id)

    num_days = int(request.GET.get('num_days', 0))
    user_date = datetime.now() - timedelta(days=num_days)
    entries = Entry.objects.filter(team=team, created_by=user, created_at__date=user_date, is_tracked=True)


    user_num_months = int(request.GET.get('num_months', 0))
    user_month = datetime.now() - relativedelta(months=user_num_months)
    for project in projects:
        project.time_for_user_and_project_and_month = get_time_for_user_and_project_and_month(team, project, user, user_month)

    context = {
        'user': user,
        'team': team,
        'latest_projects':projects[0:4],
        
        'entries': entries,

        'num_days': num_days,
        'user_date':user_date,

        'user_num_months': user_num_months,
        'user_month': user_month,

        'time_for_user_and_month': get_time_for_user_and_month(team, user, user_month),
        'time_for_user_and_date': get_time_for_user_and_date(team, user, user_date),
    }


    return render(request, 'dashboard/show_user.html', context)

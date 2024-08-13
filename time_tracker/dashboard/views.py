from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from project.models import Entry
from team.models import Team


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
# from .models import Team

# def active_team(request):
#     if request.user.is_authenticated:
#         if request.user.userprofile.active_team_id:
#             active_team = Team.objects.get(pk=request.user.userprofile.active_team_id)

#             return {'active_team': active_team}
#     return {'active_team': None }
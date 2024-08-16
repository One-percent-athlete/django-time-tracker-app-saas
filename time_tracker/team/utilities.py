from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_invitation(to_email, code, team):
    from_email = settings.DEFAULT_EMAIL_FROM
    acceptation_url = settings.ACCEPTATION_URL

    subject = 'Invitation to Time Tracker'
    text_content = 'Invitation to Time Tracker. Your code is %s' % code
    html_content = render_to_string('team/invitation_email.html', {'code': code, 'team':team, 'acceptation_url':acceptation_url})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def invitation_accepted(to_email, team, invitation):
    from_email = settings.DEFAULT_EMAIL_FROM
    subject = 'Invitation Accepted'
    text_content = 'Your Invitation Was Accepted'
    html_content = render_to_string('team/invitation_accepted.html', {'team':team, 'invitation':invitation})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [team.created_by.email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()



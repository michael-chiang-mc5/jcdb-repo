from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import *

def new_user(request):
    user = request.user
    userProfile = UserProfile(user=user,alias=user.get_username())
    userProfile.save()
    new_notification_text = 'Welcome to journalClubDB<br /> \
                            ';
    notification = Notification.constructor(user,new_notification_text)
    notification.save()
    return HttpResponseRedirect(reverse('Groups:index'))

# TODO: only user can delete notification
def deleteNotification(request, notification_pk):
    notification = Notification.objects.get(pk=notification_pk)
    notification.delete()
    return HttpResponseRedirect(reverse('Groups:index'))
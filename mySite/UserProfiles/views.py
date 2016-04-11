from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import *
from django.contrib.auth import logout

def new_user(request):
    user = request.user
    userprofile = UserProfile(user=user,alias=user.username)
    userprofile.save()
    new_notification_text = 'Welcome to journalClubDB. \
                             Detailed instructions on how to use jcdb are given \
                             <a href="http://www.michael-chiang.com/Blog/#e2">here</a>. \
                             Feel free to delete this message once you are done by \
                             clicking "delete" below.\
                            ';
    notification = Notification.constructor(user,new_notification_text)
    notification.save()
    return HttpResponseRedirect(reverse('Groups:index'))

# TODO: only user can delete notification
def deleteNotification(request, notification_pk):
    notification = Notification.objects.get(pk=notification_pk)
    notification.delete()
    return HttpResponseRedirect(reverse('Groups:index'))

def editProfileInterface(request):
    if request.user.pk==2: # guest
        logout(request)
        return HttpResponseRedirect(reverse('Groups:index'))
    context = {}
    return render(request,'UserProfiles/editProfileInterface.html',context)
def editAlias(request):
    user = request.user
    user.userprofile.alias = request.POST.get('form_text')
    user.userprofile.save()
    return HttpResponseRedirect(reverse('UserProfiles:editProfileInterface'))

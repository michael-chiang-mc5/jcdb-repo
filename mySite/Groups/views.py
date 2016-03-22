from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from Uploader.models import Document

def index(request):
    user = request.user
    # get groups that user is a member of
    groups = Group.get_groups_that_user_is_member_of(user)
    groups = groups.order_by('-time') # newest groups at the top
    # return html
    context = {'groups':groups}
    return render(request, 'Groups/index.html', context)

# methods to manage groups
def addGroupInterface(request):
    context = {}
    return render(request, 'Groups/addGroupInterface.html', context)
def addGroup(request):
    # check for user authentication, POST
    if request.method == 'POST' and request.user.is_authenticated():
        name = request.POST.get("name")
        user = request.user
    else:
        return HttpResponse("Attempted to make group without authentication or POST")
    # create group
    group = Group(name=name)
    group.save() # only need to save once
    group.admins.add(user)
    group.moderators.add(user)
    group.members.add(user)
    return HttpResponseRedirect(reverse('Groups:groupMemberView',args=[group.pk]))
# only admins can delete group
def deleteGroup(request,group_pk):
    pass
# only moderators and admins can see admin panel
def groupAdminPanel(request,group_pk):
    return HttpResponse("admin panel")
# only group members can see group view
def groupMemberView(request,group_pk):
    group = Group.objects.get(pk=group_pk)
    isModerator = group.is_moderator_or_admin(request.user)
    documents = group.document_set.all()
    documents = Document.objects.all()
    context = {'group':group,'isModerator':isModerator,'documents':documents}
    return render(request, 'Groups/groupMemberView.html', context)

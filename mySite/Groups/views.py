from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from Uploader.models import Document
from UserProfiles.models import *
from django.conf import settings
import os

# If user is logged in, show group manager. Otherwise, show landing page
def index(request):
    if request.user.is_authenticated():
        user = request.user
        # get groups that user is a member of
        groups = Group.get_groups_that_user_is_member_of(user)
        groups = groups.order_by('-time') # newest groups at the top
        # get papers that user can access
        documents = None
        for group in groups:
            if documents is None:
                documents = group.document_set.all()
            else:
                documents = documents | group.document_set.all()
        if documents:
            documents = documents.order_by('-time') # newest documents at the top
        # get notifications
        notifications = Notification.get(user)

        # return html
        context = {'groups':groups,'documents':documents,'notifications':notifications}
        return render(request, 'Groups/index.html', context)
    else:
        return HttpResponseRedirect(reverse('myContent:index'))

# html form for user adding a group
def addGroupInterface(request):
    if request.user.is_authenticated():
        context = {}
        return render(request, 'Groups/addGroupInterface.html', context)
    else:
        return HttpResponseRedirect(reverse('myContent:index'))

# user adds a group
def addGroup(request):
    # check for user authentication, POST
    if request.method == 'POST' and request.user.is_authenticated():
        name = request.POST.get("name")
        password = request.POST.get("password")
        user = request.user
    else:
        return HttpResponseRedirect(reverse('myContent:index'))
    # create group
    group = Group(name=name,password=password)
    group.save() # only need to save once
    group.admins.add(user)
    group.moderators.add(user)
    group.members.add(user)
    return HttpResponseRedirect(reverse('Groups:groupMemberView',args=[group.pk]))

# user removes self from group
def removeSelfFromGroup(request,group_pk):
    group = Group.objects.get(pk=group_pk)
    group.admins.remove(request.user)
    group.moderators.remove(request.user)
    group.members.remove(request.user)
    return HttpResponseRedirect(reverse('myContent:index'))

# delete a group. Only admins can delete group
def deleteGroup(request,group_pk):
    group = Group.objects.get(pk=group_pk)
    if group.admins.filter(pk=request.user.pk).exists() or request.user.is_superuser:
        group.delete()
        return HttpResponseRedirect(reverse('myContent:index'))
    else:
        return HttpResponseRedirect(reverse('myContent:index'))

# anybody can join a group if they know the password
def joinGroupInterface(request,group_pk):
    group = Group.objects.get(pk=group_pk)
    context = {'group':group,}
    return render(request,'Groups/joinGroupInterface.html',context)
# anybody can join a group if they know the password
def joinGroup(request,group_pk):
    name = request.POST.get("name")
    password = request.POST.get("password")
    user = request.user
    group = Group.objects.get(pk=group_pk)
    if group.password == password:
        group.members.add(user)
        return HttpResponseRedirect(reverse('Groups:groupMemberView',args=[group_pk]))
    else:
        context = {'group':group,'incorrect_password':True}
        return render(request,'Groups/joinGroupInterface.html',context)

# Make a user an admin, moderator, or member. Only admin can change permission
def changePermissions(request,user_pk,group_pk):
    # check for user authentication, POST, and make sure user is an admin of the group
    if request.method == 'POST' and request.user.is_authenticated():
        group = Group.objects.get(pk=group_pk)
        user = User.objects.get(pk=user_pk)
        permission = request.POST.get("permission")
    else:
        return HttpResponseRedirect(reverse('myContent:index'))
    if not group.admins.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('myContent:index'))
    # Change permission
    if permission == "admin":
        group.members.add(user)
        group.moderators.add(user)
        group.admins.add(user)
    elif permission == "moderator":
        group.members.add(user)
        group.moderators.add(user)
        group.admins.remove(user)
    elif permission == "member":
        group.members.add(user)
        group.moderators.remove(user)
        group.admins.remove(user)
    elif permission == "remove":
        group.members.remove(user)
        group.moderators.remove(user)
        group.admins.remove(user)
    return HttpResponseRedirect(reverse('Groups:groupAdminPanel',args=[group.pk]))

# Change name of group. Only admin can change group name
def changeGroupName(request,group_pk):
    # check for user authentication, POST, and make sure user is an admin of the group
    if request.method == 'POST' and request.user.is_authenticated():
        form_text = request.POST.get("form_text")
    else:
        return HttpResponse("Attempted to make group without authentication or POST")
    if not group.admins.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('myContent:index'))
    group = Group.objects.get(pk=group_pk)
    group.name = form_text
    group.save()
    return HttpResponseRedirect(reverse('Groups:groupAdminPanel',args=[group.pk]))

# only admin can change group description
def changeGroupDescription(request,group_pk):
    pass
# only admin can change group password
def changeGroupPassword(request,group_pk):
    # check for user authentication, POST
    if request.method == 'POST' and request.user.is_authenticated():
        form_text = request.POST.get("form_text")
    else:
        return HttpResponse("Attempted to make group without authentication or POST")
    if not group.admins.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('myContent:index'))
    group = Group.objects.get(pk=group_pk)
    group.password = form_text
    group.save()
    return HttpResponseRedirect(reverse('Groups:groupAdminPanel',args=[group.pk]))
# only admin can open and close membership
def changeAcceptingNewMembers(request,group_pk):
    pass
# only admin can change
def changeUploadApprovalRequired(request,group_pk):
    pass

# only admins can see admin panel
def groupAdminPanel(request,group_pk):
    group = Group.objects.get(pk=group_pk)
    if not group.admins.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('myContent:index'))
    admins = group.admins.all()
    moderators = group.moderators.exclude(id__in=admins)
    members = group.members.exclude(id__in=admins).exclude(id__in=moderators)
    context = {"group":group,"admins":admins,"moderators":moderators,"members":members}
    return render(request, 'Groups/groupAdminPanel.html', context)
# only moderators and admins and original uploader can see moderator panel
def documentAdminPanel(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    group = document.group
    if not group.moderators.filter(pk=request.user.pk).exists() and not request.user.is_superuser and document.user.pk != request.user.pk:
        return HttpResponseRedirect(reverse('myContent:index'))
    context = {"document":document,}
    return render(request, 'Groups/documentAdminPanel.html', context)

# only group members can see group view
def groupMemberView(request,group_pk):
    # check to make sure user is member
    group = Group.objects.get(pk=group_pk)
    if not group.members.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('myContent:index'))
    # return html
    isModerator = group.is_moderator(request.user)
    isAdmin = group.is_admin(request.user)
    documents = group.document_set.all()
    documents = documents.order_by('-time') # newest documents at the top
    context = {'group':group,'isModerator':isModerator,'isAdmin':isAdmin,'documents':documents}
    return render(request, 'Groups/groupMemberView.html', context)

# only moderators and original uploader can delete documents
def deleteDocument(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    group = document.group
    if not group.moderators.filter(pk=request.user.pk).exists() and not request.user.is_superuser and document.user.pk != request.user.pk:
        return HttpResponseRedirect(reverse('myContent:index'))
    file_path=settings.MEDIA_ROOT
    os.remove(file_path+'/'+document.docfile.name)
    document.delete()
    return HttpResponseRedirect(reverse('Groups:groupMemberView',args=[document.group.pk]))

# all members should be able to send notifications
def sendNotification(request,group_pk):
    # check for user authentication, POST
    if request.method == 'POST' and request.user.is_authenticated():
        form_text = request.POST.get("form_text")
        next_url = request.POST.get("next_url")
    else:
        return HttpResponse("Attempted to make group without authentication or POST")
    if not group.members.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponseRedirect(reverse('myContent:index'))
    # create group
    group = Group.objects.get(pk=group_pk)
    users = group.members.all()
    for user in users:
        notification = Notification.constructor(user,form_text)
        notification.save()
    return HttpResponseRedirect(next_url)

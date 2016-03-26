from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^addGroupInterface/$', views.addGroupInterface, name='addGroupInterface'),
    url(r'^addGroup/$', views.addGroup, name='addGroup'),
    url(r'^deleteGroup/(?P<group_pk>[0-9]+)/$', views.deleteGroup, name='deleteGroup'),
    url(r'^groupAdminPanel/(?P<group_pk>[0-9]+)/$', views.groupAdminPanel, name='groupAdminPanel'),
    url(r'^documentAdminPanel/(?P<document_pk>[0-9]+)/$', views.documentAdminPanel, name='documentAdminPanel'),
    url(r'^groupMemberView/(?P<group_pk>[0-9]+)/$', views.groupMemberView, name='groupMemberView'),
    url(r'^deleteGroup/(?P<group_pk>[0-9]+)/$', views.deleteGroup, name='deleteGroup'),
    url(r'^joinGroupInterface/(?P<group_pk>[0-9]+)/$', views.joinGroupInterface, name='joinGroupInterface'),
    url(r'^joinGroup/(?P<group_pk>[0-9]+)/$', views.joinGroup, name='joinGroup'),
    url(r'^index/$', views.index, name='index'),
    url(r'^makeUserAdmin/(?P<user_pk>[0-9]+)/(?P<group_pk>[0-9]+)/$', views.makeUserAdmin, name='makeUserAdmin'),
    url(r'^makeUserModerator/(?P<user_pk>[0-9]+)/(?P<group_pk>[0-9]+)/$', views.makeUserModerator, name='makeUserModerator'),
    url(r'^makeUserMember/(?P<user_pk>[0-9]+)/(?P<group_pk>[0-9]+)/$', views.makeUserMember, name='makeUserMember'),
    url(r'^makeUserRemoved/(?P<user_pk>[0-9]+)/(?P<group_pk>[0-9]+)/$', views.makeUserRemoved, name='makeUserRemoved'),
    url(r'^changeGroupName/(?P<group_pk>[0-9]+)/$', views.changeGroupName, name='changeGroupName'),
    url(r'^changeGroupDescription/(?P<group_pk>[0-9]+)/$', views.changeGroupDescription, name='changeGroupDescription'),
    url(r'^changeGroupPassword/(?P<group_pk>[0-9]+)/$', views.changeGroupPassword, name='changeGroupPassword'),
    url(r'^changeAcceptingNewMembers/(?P<group_pk>[0-9]+)/$', views.changeAcceptingNewMembers, name='changeAcceptingNewMembers'),
    url(r'^changeUploadApprovalRequired/(?P<group_pk>[0-9]+)/$', views.changeUploadApprovalRequired, name='changeUploadApprovalRequired'),

    url(r'^deleteDocument/(?P<document_pk>[0-9]+)/$', views.deleteDocument, name='deleteDocument'),
    url(r'^sendNotification/(?P<group_pk>[0-9]+)/$', views.sendNotification, name='sendNotification'),

]

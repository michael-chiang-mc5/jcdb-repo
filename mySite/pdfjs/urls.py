from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^viewer/(?P<document_pk>[0-9]+)/$', views.viewer, name='viewer'),
    url(r'^viewer_raw/(?P<document_pk>[0-9]+)/$', views.viewer_raw, name='viewer_raw'),
    url(r'^viewer_notes/(?P<document_pk>[0-9]+)/$', views.viewer_notes, name='viewer_notes'),
    url(r'^addNote/$', views.addNote, name='addNote'),
    url(r'^replyNote/$', views.replyNote, name='replyNote'),
    url(r'^editNotetext/$', views.editNotetext, name='editNotetext'),
    url(r'^deleteNotetext/$', views.deleteNotetext, name='deleteNotetext'),
    url(r'^getNotesJson/(?P<document_pk>[0-9]+)/$', views.getNotesJson, name='getNotesJson'),

]

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^canvas/$', views.canvas, name='canvas'),
    url(r'^draw/$', views.draw, name='draw'),
    url(r'^iframe_overlay/$', views.iframe_overlay, name='iframe_overlay'),
    url(r'^viewer/(?P<document_pk>[0-9]+)$', views.viewer, name='viewer'),
]

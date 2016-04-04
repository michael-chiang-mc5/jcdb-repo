from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from pdfjs.views import viewer

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('Groups:index'))
    else:
        context = {}
        return render(request, 'myContent/index.html', context)

def demo(request):
    logout(request)
    user = authenticate(username="guest", password="guestguest")
    login(request, user)
    return viewer(request,1)

def jcdb_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myContent:index'))

def faq(request):
    if request.user.pk==2: # guest
        logout(request)
        return HttpResponseRedirect(reverse('Groups:index'))
    else:
        context = {}
        return render(request, 'myContent/faq.html', context)

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('Groups:index'))
    else:
        context = {}
        return render(request, 'myContent/index.html', context)

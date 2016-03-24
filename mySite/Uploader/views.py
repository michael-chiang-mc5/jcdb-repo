from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from Groups.models import Group
from .models import Document
from .forms import DocumentForm

def uploadInterface(request,group_pk):
    context = {"group_pk":group_pk,}
    return render(request, 'Uploader/uploadInterface.html',context)

def upload(request):
    # TODO: make sure file is pdf
    if request.method == 'POST' and request.user.is_authenticated():
        user = request.user
        f = request.FILES['docfile']
        group_pk = request.POST.get("group_pk")
        next_url = request.POST.get("next_url")
    document = Document(docfile = f, user=user)
    document.group = Group.objects.get(pk=group_pk)
    document.save()
    return HttpResponseRedirect(next_url)

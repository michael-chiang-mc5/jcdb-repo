from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from Groups.models import Group
from .models import Document
from .forms import DocumentForm

import os
from django.conf import settings

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
    document = Document(docfile = f)
    document.group = Group.objects.get(pk=group_pk)
    document.save()
    return HttpResponseRedirect(next_url)

def list(request):
    #root="/media/"
    #Path=settings.MEDIA_ROOT
    #os.chdir(Path)
    #for files in os.listdir("."):
    #    if files[-3:].lower() in ["gif","png","jpg","bmp"] :
    #        return HttpResponse(files)


    documents = Document.objects.all().order_by('-time')
    context = {'documents':documents}
    return render(request, 'Uploader/list.html',context)


def delete(request,document_pk):

    doc = Document.objects.get(pk=document_pk)
    file_path=settings.MEDIA_ROOT
    os.remove(file_path+'/'+doc.docfile.name)
    doc.delete()
    return HttpResponseRedirect( reverse('Uploader:list') )

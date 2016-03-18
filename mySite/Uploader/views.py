from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import Document
from .forms import DocumentForm

import os
from django.conf import settings

def upload(request):
    # TODO: make sure user logged in
    # TODO: make sure file is pdf
    f = request.FILES['docfile']
    newdoc = Document(docfile = f)
    newdoc.save()
    return redirect(request.GET['next'])

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

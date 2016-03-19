from django.shortcuts import render
from django.http import HttpResponse
from Uploader.views import Document
from django.conf import settings

def index(request):
    context = {}
    return render(request, 'pdfjs/index.html', context)

def viewer(request,document_pk):
    context = {'document_pk':document_pk}
    return render(request, 'pdfjs/viewer_iframe.html', context)

def viewer_raw(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    pdf_url = settings.MEDIA_URL + document.docfile.name
    context = {'pdf_url':pdf_url}
    return render(request, 'pdfjs/viewer_original.html', context)

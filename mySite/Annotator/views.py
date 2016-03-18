from django.shortcuts import render
from django.http import HttpResponse
from Uploader.views import Document
from django.conf import settings
import PyPDF2
from PyPDF2 import PdfFileReader

def index(request):
    context = {}
    return render(request, 'Annotator/index.html', context)

def canvas(request):
    context = {}
    return render(request, 'Annotator/canvas.html', context)

def draw(request):
    context = {}
    return render(request, 'Annotator/draw.html', context)

def iframe_overlay(request):
    context = {}
    return render(request, 'Annotator/iframe_overlay.html', context)

def viewer0(request):
    context = {}
    return render(request, 'Annotator/viewer.html', context)


def viewer(request,document_pk):
    # get pdf document
    document = Document.objects.get(pk=document_pk)
    # get number of pages in pdf
    url = settings.BASE_DIR + document.docfile.url
    reader = PyPDF2.PdfFileReader(url)
    num_pages = reader.getNumPages()


    context = {'document':document,'num_pages':num_pages}
    return render(request, 'Annotator/viewer.html', context)

from django.shortcuts import render
from django.http import HttpResponse
from Uploader.views import Document
from django.conf import settings
from django.http import JsonResponse

def index(request):
    context = {}
    return render(request, 'pdfjs/index.html', context)

def viewer(request,document_pk):
    context = {'document_pk':document_pk}
    return render(request, 'pdfjs/viewer_iframe.html', context)

def viewer_raw(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    pdf_url = settings.MEDIA_URL + document.docfile.name
    context = {'pdf_url':pdf_url,'document_pk':document_pk}
    return render(request, 'pdfjs/viewer_original.html', context)

def addNote(request):
    if request.method == 'POST':
        document_pk = request.POST.get("document_pk")
        form_text = request.POST.get("form_text")
        user = request.user.username
        response = {'document_pk':document_pk,}
        return JsonResponse(response)
    else:
        return HttpResponse("Attempted to add note without POST")

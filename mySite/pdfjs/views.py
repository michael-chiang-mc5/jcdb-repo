from django.shortcuts import render
from django.http import HttpResponse
from Uploader.models import Document
from django.conf import settings
from django.http import JsonResponse
from .models import *

def index(request):
    notes = Note.objects.all()
    noteTexts = NoteText.objects.all()
    context = {'notes':notes,'noteTexts':noteTexts}
    return render(request, 'pdfjs/index.html', context)

def viewer(request,document_pk):
    context = {'document_pk':document_pk}
    return render(request, 'pdfjs/viewer_iframe.html', context)

def viewer_raw(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    pdf_url = settings.MEDIA_URL + document.docfile.name
    notes = Note.objects.filter(document=document)

    context = {'pdf_url':pdf_url,'document_pk':document_pk,"notes":notes}
    return render(request, 'pdfjs/viewer_original.html', context)

def addNote(request):
    if request.method == 'POST':
        document_pk = request.POST.get("document_pk")
        form_text = request.POST.get("form_text")
        user = request.user
        page_number = request.POST.get("page_number")
        x_normalized = request.POST.get("x_normalized")
        y_normalized = request.POST.get("y_normalized")
        width = request.POST.get("width")
        height = request.POST.get("height")

        note = Note(user=user,
                    document=Document.objects.get(pk=document_pk),
                    page_number=page_number,
                    x_normalized_position=x_normalized,
                    y_normalized_position=y_normalized,
                    width=width,
                    height=height,)
        note.save()
        note.addText(user=user,text=form_text)
        response = {'document_pk':document_pk,}
        return JsonResponse(response)
    else:
        return HttpResponse("Attempted to add note without POST")

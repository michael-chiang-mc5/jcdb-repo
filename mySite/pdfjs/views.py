from django.shortcuts import render
from django.http import HttpResponse
from Uploader.models import Document
from django.conf import settings
from django.http import JsonResponse
from .models import *
from django.core.urlresolvers import reverse

def index(request):
    notes = Note.objects.all()
    noteTexts = NoteText.objects.all()
    context = {'notes':notes,'noteTexts':noteTexts}
    return render(request, 'pdfjs/index.html', context)

def viewer(request,document_pk):
    context = {'document_pk':document_pk}
    return render(request, 'pdfjs/viewer_iframe.html', context)

# View for rendering pdf in iframe #1
def viewer_raw(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    pdf_url = settings.MEDIA_URL + document.docfile.name
    addnote_url = reverse('pdfjs:addNote')
    getnotesjson_url = reverse('pdfjs:getNotesJson', args=[document_pk])
    notes = Note.objects.filter(document=document)
    context = {'pdf_url':pdf_url,'addnote_url':addnote_url,'getnotesjson_url':getnotesjson_url,'document_pk':document_pk,"notes":notes}
    return render(request, 'pdfjs/viewer_original.html', context)
# View for rendering notes in iframe #2
def viewer_notes(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    notes = Note.objects.filter(document=document)
    context = {'document_pk':document_pk,"notes":notes}
    return render(request, 'pdfjs/viewer_notes.html', context)

# serializes notes to JsonResponse
# This view is called when client wants to update knowledge of note database
# [note_obj1, note_obj2, ...]
#   note_obj.page_number
#   note_obj.x_normalized_position
#   note_obj.note_text_obj
#     note_obj.note_text_obj.text
def getNotesJson(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    notes = Note.objects.filter(document=document)
    json_obj = []
    for note in notes:
        notetexts = note.notetext_set.all() # TODO: sort by time
        note_text = []
        for notetext in notetexts:
            obj2 = {'user':notetext.user.username,
                    'time':notetext.time,
                    'text':notetext.text,
                    }
            note_text.append(obj2)
        obj =   {'page_number':note.page_number,
                'x_normalized_position':note.x_normalized_position,
                'y_normalized_position':note.y_normalized_position,
                'width':note.width,
                'height':note.height,
                'note_text':note_text,
                }
        json_obj.append(obj)
    return JsonResponse(json_obj, safe=False)

def replyNote(request):
    if request.method == 'POST':
        note_pk = request.POST.get("note_pk")
        form_text = request.POST.get("form_text")
        user = request.user
    else:
        return HttpResponse("Attempted to reply note without POST")
    note = Note.objects.get(pk=note_pk)
    note.addText(user=user,text=form_text)
    response = {}
    return JsonResponse(response)

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
    else:
        return HttpResponse("Attempted to add note without POST")
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

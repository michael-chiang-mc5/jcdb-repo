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
    dragnote_url = reverse('pdfjs:dragNote')
    resizenote_url = reverse('pdfjs:resizeNote')
    #getnotesjson_url = reverse('pdfjs:getNotesJson', args=[document_pk]) # deprecate
    notes_json = Note.getNotesJson(document_pk)
    #context = {'pdf_url':pdf_url,'addnote_url':addnote_url,'getnotesjson_url':getnotesjson_url,'notes_json':notes_json,'document_pk':document_pk}
    context = {'pdf_url':pdf_url,'addnote_url':addnote_url,'dragnote_url':dragnote_url,'resizenote_url':resizenote_url,'notes_json':notes_json,'document_pk':document_pk}
    return render(request, 'pdfjs/viewer_original.html', context)
# View for rendering notes in iframe #2
def viewer_notes(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    notes = Note.objects.filter(document=document)
    url_deletenotetext = reverse('pdfjs:deleteNotetext');
    url_editNotetext = reverse('pdfjs:editNotetext')
    url_replynote = reverse('pdfjs:replyNote')
    context = {'document_pk':document_pk,"notes":notes,"url_deletenotetext":url_deletenotetext,'url_editNotetext':url_editNotetext,'url_replynote':url_replynote}
    return render(request, 'pdfjs/viewer_notes.html', context)

# serializes notes to JsonResponse
# This view is called when client wants to update knowledge of note database
# [note_obj1, note_obj2, ...]
#   note_obj.page_number
#   note_obj.x_normalized_position
#   note_obj.note_text_obj
#     note_obj.note_text_obj.text
# Deprecated
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
        obj =   {'pk':note.pk,
                'page_number':note.page_number,
                'x_normalized_position':note.x_normalized_position,
                'y_normalized_position':note.y_normalized_position,
                'width_normalized':note.width_normalized,
                'height_normalized':note.height_normalized,
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
    notetext = note.addText(user=user,text=form_text)
    notetext_obj = NoteText.getNotetextJson(notetext)
    response = {'notetext_obj':notetext_obj,'note_pk':note.pk}
    return JsonResponse(response)

# return json object representing the note added
def addNote(request):
    if request.method == 'POST':
        document_pk = request.POST.get("document_pk")
        form_text = request.POST.get("form_text")
        user = request.user
        page_number = request.POST.get("page_number")
        x_normalized = request.POST.get("x_normalized")
        y_normalized = request.POST.get("y_normalized")
        width_normalized = request.POST.get("width_normalized")
        height_normalized = request.POST.get("height_normalized")
    else:
        return HttpResponse("Attempted to add note without POST")
    note = Note(user=user,
                document=Document.objects.get(pk=document_pk),
                page_number=page_number,
                x_normalized_position=x_normalized,
                y_normalized_position=y_normalized,
                width_normalized=width_normalized,
                height_normalized=height_normalized,)
    note.save()
    note.addText(user=user,text=form_text)
    note_obj = Note.getNoteJson(note)
    response = {'note_obj':note_obj}
    return JsonResponse(response)

def editNotetext(request):
    if request.method == 'POST':
        notetext_pk = request.POST.get("notetext_pk")
        form_text = request.POST.get("form_text")
        user = request.user
    else:
        return HttpResponse("Attempted to reply note without POST")
    notetext = NoteText.objects.get(pk=notetext_pk)
    notetext.editText(text=form_text)
    note_pk = notetext.note.pk
    isFirst = notetext.isFirst()
    response = {'isFirst':isFirst,'form_text':form_text,'pk':notetext_pk,'note_pk':note_pk}
    return JsonResponse(response)

def deleteNotetext(request):
    if request.method == 'POST':
        notetext_pk = request.POST.get("notetext_pk")
    else:
        return HttpResponse("Attempted to reply note without POST")
    notetext = NoteText.objects.get(pk=notetext_pk)
    # Remove entier note if notetext is first
    isFirst = notetext.isFirst()
    if isFirst:
        note = notetext.note
        note.delete()
    else:
        notetext.delete()
    response = {'delete_entire_note':isFirst}
    return JsonResponse(response)

def resizeNote(request):
    if request.method == 'POST':
        width_normalized = request.POST.get("width_normalized")
        height_normalized = request.POST.get("height_normalized")
        note_pk = request.POST.get("note_pk")
    else:
        return HttpResponse("Attempted to resize note without POST")
    note = Note.objects.get(pk=note_pk)
    note.width_normalized = width_normalized
    note.height_normalized = height_normalized
    note.save()
    response = {}
    return JsonResponse(response)

def dragNote(request):
    if request.method == 'POST':
        x_normalized = request.POST.get("x_normalized")
        y_normalized = request.POST.get("y_normalized")
        note_pk = request.POST.get("note_pk")
    else:
        return HttpResponse("Attempted to resize note without POST")
    note = Note.objects.get(pk=note_pk)
    note.x_normalized_position = x_normalized
    note.y_normalized_position = y_normalized
    note.save()
    response = {}
    return JsonResponse(response)

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from Uploader.models import Document
from django.conf import settings
from django.http import JsonResponse
from .models import *
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache

def index(request):
    notes = Note.objects.all()
    noteTexts = NoteText.objects.all()
    context = {'notes':notes,'noteTexts':noteTexts}
    return render(request, 'pdfjs/index.html', context)

@never_cache
def viewer(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    group = document.group
    if group.members.filter(pk=request.user.pk).exists() or request.user.is_superuser:
        context = {'document_pk':document_pk}
        return render(request, 'pdfjs/viewer_iframe.html', context)
    else:
        return HttpResponseRedirect(reverse('myContent:index'))

# View for rendering pdf in iframe #1
@never_cache
def viewer_pdf(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    group = document.group
    if group.members.filter(pk=request.user.pk).exists() or request.user.is_superuser:
        pdf_url = settings.MEDIA_URL + document.docfile.name
        addnote_url = reverse('pdfjs:addNote')
        dragnote_url = reverse('pdfjs:dragNote')
        resizenote_url = reverse('pdfjs:resizeNote')
        notes_json = Note.getNotesJson(document_pk)
        context = {'pdf_url':pdf_url,'addnote_url':addnote_url,'dragnote_url':dragnote_url,'resizenote_url':resizenote_url,'notes_json':notes_json,'document_pk':document_pk}
        return render(request, 'pdfjs/viewer_pdf.html', context)
    else:
        return HttpResponseRedirect(reverse('myContent:index'))

# View for rendering notes in iframe #2
@never_cache
def viewer_notes(request,document_pk):
    document = Document.objects.get(pk=document_pk)
    group = document.group
    if group.members.filter(pk=request.user.pk).exists() or request.user.is_superuser:
        notes = Note.objects.filter(document=document)
        url_deletenotetext = reverse('pdfjs:deleteNotetext');
        url_editNotetext = reverse('pdfjs:editNotetext')
        url_replynote = reverse('pdfjs:replyNote')
        context = {'document_pk':document_pk,"notes":notes,"url_deletenotetext":url_deletenotetext,'url_editNotetext':url_editNotetext,'url_replynote':url_replynote}
        return render(request, 'pdfjs/viewer_notes.html', context)
    else:
        return HttpResponseRedirect(reverse('myContent:index'))

def replyNote(request):
    if request.method == 'POST':
        note_pk = request.POST.get("note_pk")
        form_text = request.POST.get("form_text")
        user = request.user
    else:
        return HttpResponse("Attempted to reply note without POST")
    note = Note.objects.get(pk=note_pk)
    group = note.document.group
    if not group.members.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponse("You are trying to reply to a note in a group you do not belong to")
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
        document = Document.objects.get(pk=document_pk)
        group = document.group
    else:
        return HttpResponse("Attempted to add note without POST")
    if not group.members.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponse("You are trying to add a note in a group you do not belong to")
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
    group = notetext.note.document.group
    if not group.moderators.filter(pk=request.user.pk).exists() and not notetext.user == request.user and not request.user.is_superuser:
        return HttpResponse("You are trying to edit a note and you are not a moderator / note owner")
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
    group = notetext.note.document.group
    if not group.moderators.filter(pk=request.user.pk).exists() and not notetext.user == request.user and not request.user.is_superuser:
        return HttpResponse("You are trying to edit a note and you are not a moderator / note owner")
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
    group = note.document.group
    if not group.members.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponse("You are trying to resize a note in a group you do not belong to")
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
    group = note.document.group
    if not group.members.filter(pk=request.user.pk).exists() and not request.user.is_superuser:
        return HttpResponse("You are trying to resize a note in a group you do not belong to")
    note.x_normalized_position = x_normalized
    note.y_normalized_position = y_normalized
    note.save()
    response = {}
    return JsonResponse(response)

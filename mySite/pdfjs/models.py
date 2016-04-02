from django.db import models
from django.contrib.auth.models import User
from Uploader.models import Document
from UserProfiles.models import UserProfile

class Note(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document)
    page_number = models.PositiveIntegerField()
    x_normalized_position = models.FloatField()
    y_normalized_position = models.FloatField()
    width_normalized = models.FloatField()
    height_normalized = models.FloatField()

    class Meta:
        ordering = ['page_number', 'y_normalized_position']

    def __str__(self):
        return str(self.pk)
    def addText(self,user,text):
        self.save()
        noteText = NoteText(user=user,text=text,note=self)
        noteText.save()
        return noteText

    # get all notes in a given document. return as json object
    def getNotesJson(document_pk):
        document = Document.objects.get(pk=document_pk)
        notes = Note.objects.filter(document=document)
        json_obj = []
        for note in notes:
            obj = Note.getNoteJson(note)
            json_obj.append(obj)
        return json_obj
    def getNoteJson(note):
        notetexts = note.notetext_set.all() # TODO: sort by time
        note_text = []
        for notetext in notetexts:
            obj2 = NoteText.getNotetextJson(notetext)
            note_text.append(obj2)
        obj =   {'pk':note.pk,
                'page_number':note.page_number,
                'x_normalized_position':note.x_normalized_position,
                'y_normalized_position':note.y_normalized_position,
                'width_normalized':note.width_normalized,
                'height_normalized':note.height_normalized,
                'note_text':note_text,
                }
        return obj

class NoteText(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    note = models.ForeignKey(Note)
    def __str__(self):
        return self.text
    def getNotetextJson(notetext):
        obj = {'username':notetext.user.userprofile.getName(),
                'time':notetext.time.strftime('%m-%d-%Y'), # TODO: switch to age
                'text':notetext.text,
                'pk':notetext.pk,
                }
        return obj
    def editText(self,text):
        self.text=text;
        self.save();
    # returns True if notetext object if first in Note
    def isFirst(self):
        note = self.note
        notetexts = note.notetext_set.order_by('time')
        first_pk = notetexts[0].pk
        if first_pk == self.pk:
            return True
        else:
            return False

from django.db import models
from django.contrib.auth.models import User
from Uploader.models import Document

class Note(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document)
    page_number = models.PositiveIntegerField()
    x_normalized_position = models.FloatField()
    y_normalized_position = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return str(self.page_number)
    def addText(self,user,text):
        self.save()
        noteText = NoteText(user=user,text=text,note=self)
        noteText.save()


class NoteText(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    note = models.ForeignKey(Note)
    def __str__(self):
        return self.text

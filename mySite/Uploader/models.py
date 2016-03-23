from django.db import models
from Groups.models import Group
from django.contrib.auth.models import User

class Document(models.Model):
    docfile = models.FileField(upload_to='')
    time = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group)
    approved = models.BooleanField(default=True)
    user = models.ForeignKey(User)

    title = models.TextField(blank=True,null=True)
    authors = models.TextField(blank=True,null=True)
    journal = models.TextField(blank=True,null=True)
    year = models.IntegerField(blank=True,null=True)

    def getTitle(self):
        if not self.title:
            return self.docfile.name[2:]

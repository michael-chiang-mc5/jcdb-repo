from django.db import models
from Groups.models import Group

class Document(models.Model):
    docfile = models.FileField(upload_to='')
    time = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group)
    approved = models.BooleanField(default=True)

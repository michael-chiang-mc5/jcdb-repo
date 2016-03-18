from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='')
    time = models.DateTimeField(auto_now_add=True)

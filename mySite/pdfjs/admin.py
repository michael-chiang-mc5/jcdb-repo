from django.contrib import admin

from .models import *



class NoteTextInline(admin.StackedInline):
    model = NoteText
    extra = 0

class NoteTextAdmin(admin.ModelAdmin):
    inlines = [ NoteTextInline, ]

admin.site.register(Note, NoteTextAdmin)

from django.contrib import admin

from .models import UserProfile, Notification

admin.site.register(UserProfile)
admin.site.register(Notification)

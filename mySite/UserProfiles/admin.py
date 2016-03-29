from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Notification

admin.site.register(UserProfile)
admin.site.register(Notification)

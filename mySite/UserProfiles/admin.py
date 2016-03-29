from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Notification
from django.contrib.auth.models import User

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]

admin.site.register(User, UserProfileAdmin)
admin.site.register(Notification)

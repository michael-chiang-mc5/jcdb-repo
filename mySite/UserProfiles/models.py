from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    alias = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(user)
    def getName(self):
        if self.alias:
            return self.alias
        else:
            return user.get_username()

class Notification(models.Model):
    userProfile = models.ForeignKey(UserProfile)
    text = models.TextField()
    def __str__(self):
        return str(self.text)
    def constructor(user,text):
        userProfile = UserProfile.objects.get(user=user)
        return Notification(userProfile=userProfile,text=text)
    def get(user):
        notifications = Notification.objects.filter(userProfile__user=user)
        return notifications

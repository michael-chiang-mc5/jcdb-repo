from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.TextField()
    description = models.TextField(blank=True)
    time = models.DateTimeField(auto_now_add=True)
    password = models.TextField(blank=True)
    openForNewMembers = models.BooleanField(default=True)
    uploadApprovalRequired = models.BooleanField(default=False)

    admins     = models.ManyToManyField(User, blank=True, related_name="admin_of_groups")
    moderators = models.ManyToManyField(User, blank=True, related_name="mod_of_groups")
    members    = models.ManyToManyField(User, blank=True, related_name="member_of_groups") # to access groups from User instance, user.member_of_groups.all()


    def __str__(self):
        return str(self.name)
    def get_groups_that_user_is_member_of(user):
        return user.member_of_groups.all()
    def is_moderator_or_admin(self,user):
        isAdmin = self.admins.filter(pk=user.pk).exists()
        isModerator = self.moderators.filter(pk=user.pk).exists()
        return isAdmin or isModerator

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(default='profile_pic.png',
                                    upload_to='profile_pics', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Profile"

from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    bio=models.TextField(blank=True,null=True)
    twitter_id=models.CharField(max_length=100,blank=True,null=True)
    github_id = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.ImageField(default='profile_pic.png',
                                    upload_to='profile_pics', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Profile"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300 :
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)




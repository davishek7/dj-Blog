from django.db import models

# Create your models here.
class Notification(models.Model):
    post = models.ForeignKey(
        Post,related_name='notifications', on_delete=models.DO_NOTHING, blank=True, null=True)
    comment = models.ForeignKey(
        Comment,related_name='notifications', on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status=models.IntegerField(default=1)
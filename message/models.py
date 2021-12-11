from django.db import models

# Create your models here.
class Message(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    

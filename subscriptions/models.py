from django.db import models

# Create your models here.
class Subscribe(models.Model):
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email
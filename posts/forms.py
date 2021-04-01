from django import forms
from django.forms import ModelForm
from .models import Comment

class NewCommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['body']


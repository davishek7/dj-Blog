from django import forms
from django.forms import ModelForm
from .models import Comment,Post,Category
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class NewCommentForm(forms.ModelForm):
    # body = RichTextFormField(config_name='comment',required=True)
    body=forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    class Meta:
        model=Comment
        fields=['body']

class PostForm(forms.ModelForm):
    title=forms.CharField(required=True)
    category=forms.ModelChoiceField(queryset=Category.objects.all(),required=True)
    content=RichTextUploadingFormField(required=True)
    status=forms.CharField(widget=forms.Select(choices=Post.options),required=True)

    class Meta:
        model=Post
        fields=['title','category','content','status']



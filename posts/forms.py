from django import forms
from django.forms import ModelForm
from .models import Comment,Post,Category
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField

choices=Category.objects.all().values_list('name','name')
choice_list=[]
for item in choices:
    choice_list.append(item)

class NewCommentForm(forms.ModelForm):
    body = RichTextFormField(config_name='comment',required=True)
    class Meta:
        model=Comment
        fields=['body']

class PostForm(forms.ModelForm):
    title=forms.CharField(required=True)
    category=forms.CharField(widget=forms.Select(choices=choice_list))
    content=RichTextUploadingFormField(required=True)
    status=forms.CharField(widget=forms.Select(choices=Post.options),required=True)

    class Meta:
        model=Post
        fields=['title','category','content','status']



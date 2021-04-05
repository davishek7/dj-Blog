from django import forms
from django.forms import ModelForm
from .models import Comment,Post,Category
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class NewCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for fieldname in ['name', 'email', 'content']:
            self.fields[fieldname].required=True

    class Meta:
        model=Comment
        fields=['name','email','content']

class PostForm(forms.ModelForm):
    title=forms.CharField(required=True)
    category=forms.ModelChoiceField(queryset=Category.objects.all(),required=True)
    content=RichTextUploadingFormField(required=True)
    status=forms.CharField(widget=forms.Select(choices=Post.options),required=True)

    class Meta:
        model=Post
        fields=['title','category','content','status']



from django import forms
from django.forms import ModelForm
from .models import Comment,Post,Category
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class NewCommentForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your name'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Your comment'}))

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for fieldname in ['name', 'email', 'content']:
            self.fields[fieldname].required=True
            self.fields['email'].help_text='<small class="text-muted">* Your email will not be published.</small>'

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



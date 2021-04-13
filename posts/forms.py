from django import forms
from django.forms import ModelForm
from .models import Comment,Post,Category
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class NewCommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email', 'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Your comment','class':'form-control'}))

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for fieldname in ['name', 'email', 'content']:
            self.fields[fieldname].required=True
            self.fields[fieldname].label = ''
            self.fields['email'].help_text='<small class="text-muted">* Your email will not be published.</small>'

    class Meta:
        model=Comment
        fields=['name','email','content']

class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=True, empty_label="----Select Category----", widget=forms.Select(attrs={'class': 'form-control'}))
    content = RichTextUploadingFormField(required=True, widget=forms.Textarea(
        attrs={ 'class': 'form-control'}))
    status = forms.CharField(widget=forms.Select(choices=Post.options, attrs={
                             'class': 'form-control'}), required=True)

    class Meta:
        model=Post
        fields=['title','category','content','status']

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter category name'}), required=True)

    class Meta:
        model = Category
        fields=['name']

class SearchForm(forms.Form):
    q = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Search for Post'}),required=True)



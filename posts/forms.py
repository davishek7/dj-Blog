from django import forms
from django.forms import ModelForm
from .models import Comment, Post, Category, Subscribe, Tag
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingFormField


class NewCommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Your name', 'class': 'form-control mb-2'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email', 'class': 'form-control mb-2'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'rows': 5, 'placeholder': 'Your comment', 'class': 'form-control mb-2'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['name', 'email', 'content']:
            self.fields[fieldname].required = True
            self.fields[fieldname].label = ''
            self.fields['email'].help_text = '<small class="text-muted">* Your email will not be published.</small>'

    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']


class PostForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=True, empty_label="----Select Category----", widget=forms.Select(attrs={'class': 'form-control w-50'}))
    content = RichTextUploadingFormField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control'}))
    status = forms.CharField(widget=forms.Select(choices=Post.options, attrs={
                             'class': 'form-control w-50'}), required=True)

    tags = forms.ModelMultipleChoiceField(required=True, queryset=Tag.objects.all(
    ), widget=forms.SelectMultiple(attrs={'class': 'form-control w-50'}))

    class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'content', 'status', 'tags']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter category name'}), required=True)

    class Meta:
        model = Category
        fields = ['name']


class SearchForm(forms.Form):
    q = forms.CharField(label='',
                        widget=forms.TextInput(
                            attrs={'class': 'form-control', 'placeholder': 'Search for Post'}),
                        required=True)


class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(label='', required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Please enter your email', 'class': 'form-control', 'id': 'susbsribe-email'}))

    class Meta:
        model = Subscribe
        fields = ['email']

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data['email']
        if Subscribe.objects.filter(email=email).exists():
            raise forms.ValidationError('You\'ve alreday subscribed!')
        return email

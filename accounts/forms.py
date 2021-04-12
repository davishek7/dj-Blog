from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self,*args,**kwargs):
        super(CreateUserForm,self).__init__(*args,**kwargs)

        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text=None
    
    def clean(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exist!')
        return self.cleaned_data

class UserLoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['username','password']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), required=True)
    twitter_id=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    github_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=False)
    class Meta:
        model = Profile
        fields = ['bio', 'twitter_id', 'github_id', 'profile_pic']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}), required=True)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']

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

    def clean(self):
        username=self.cleaned_data.get('username')
        email=self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        return email

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists!')
        return username

class UserLoginForm(AuthenticationForm):
    class Meta:
        model=User
        fields=['username','password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username does not exist!')
        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    bio=forms.CharField(widget=forms.Textarea(attrs={'rows':3}),required=True)
    class Meta:
        model = Profile
        fields = ['bio','profile_pic']

class UserUpdateForm(forms.ModelForm):
    first_name=forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model=User
        fields=['first_name','last_name']

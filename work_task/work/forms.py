from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from . import models
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrong':
            raise ValidationError('Wrong password!')
        return data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username']

    def clean_password_check(self):
        data = self.cleaned_data['password']
        if data != self.cleaned_data['password_check']:
            raise ValidationError('Password missmatch')
        return self.cleaned_data['password_check']

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        data = super().save(commit)
        data.set_password(self.cleaned_data['password'])
        return data

from django import forms
from .models import Doctor
from django.contrib.auth.models import User


class DocForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class DocProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('name', 'phone', 'photo', 'degree_copy', 'gender',)

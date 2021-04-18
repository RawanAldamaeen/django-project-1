from django import forms
from base.models import Doctor

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class DocForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class DocProfileForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ('name', 'phone', 'photo', 'degree_copy', 'gender',)


from django import forms
from base.models import Patient

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class PatForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class PatProfileForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ('name', 'phone', 'photo', 'gender',)


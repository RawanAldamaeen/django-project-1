from django import forms
from .models import Patient
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientForm(forms.ModelForm):
    username = forms.CharField(min_length=8)
    email = forms.EmailField(validators=[validators.validate_email])
    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[validate_password])
    name = forms.CharField(validators=[validators.MinLengthValidator(2)])
    phone = forms.IntegerField()
    photo = forms.ImageField()

    class Meta:
        model = Patient
        fields = ('name', 'phone', 'photo', 'gender')

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("We have a user with this user email-id")
        return data

    def validate_password(self, password):
        user = self.context['request'].user
        validate_password(password, user=user)
        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if int(phone):
            min_length = 9
            max_length = 12
            ph_length = str(phone)
            if len(ph_length) < min_length or len(ph_length) > max_length:
                raise ValidationError('Phone number length not valid')

        if Patient.objects.filter(phone=phone).count() > 0:
            raise forms.ValidationError("We have a user with this user phone")

        return phone


class LoginForm(forms.ModelForm):

    username = forms.CharField(min_length=8)
    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password')

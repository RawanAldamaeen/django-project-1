from django import forms
from .models.doctor import Doctor
from .models.specialty import Specialty
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError

User = get_user_model()


class DocForm(forms.ModelForm):
    username = forms.CharField(min_length=8)
    email = forms.EmailField(validators=[validators.validate_email])
    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[validate_password])
    name = forms.CharField(validators=[validators.MinLengthValidator(2)])
    phone = forms.CharField()
    photo = forms.ImageField()
    degree_copy = forms.ImageField()
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all())

    class Meta:
        model = Doctor
        fields = ('name', 'phone', 'photo', 'degree_copy', 'gender', 'language')

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

        if phone:
            min_length = 9
            max_length = 12
            if len(phone) < min_length or len(phone) > max_length:
                raise ValidationError('Phone number length not valid')

        if Doctor.objects.filter(phone=phone).count() > 0:
            raise forms.ValidationError("We have a user with this user phone")

        return phone

class LoginForm(forms.ModelForm):

    username = forms.CharField(min_length=8)
    password = forms.CharField(widget=forms.PasswordInput(),
                               validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password')


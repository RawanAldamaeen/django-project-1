
from base.models import User
from django.db import models
from django.utils.translation import gettext as _


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=15)
    photo = models.ImageField(upload_to='patient/patient_pics', blank=True, default='')
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='None', max_length=32)
    language = models.CharField(choices=[('ar', _('Arabic')), ('en', _('English'))], default='en', max_length=32)

    def __str__(self):
        return f'{self.user.username} Profile'
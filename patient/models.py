from django.db import models
from base.modeld import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.IntegerField(unique=True)
    photo = models.ImageField(upload_to='patient/patient_pics', blank=True, default='')
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='None', max_length=32)

    def __str__(self):
        return f'{self.user.username} Profile'
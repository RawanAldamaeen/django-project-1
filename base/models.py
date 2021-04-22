
from django.conf import settings
from django.core import validators
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils import translation


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)


class Specialty(models.Model):
    specialty = models.CharField(max_length=100)
    specialty_ar = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.specialty


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.IntegerField(unique=True)
    photo = models.ImageField(upload_to='doctors/dr_pics', blank=True, default='')
    degree_copy = models.ImageField(upload_to='doctors/dr_degree_copy', default=' ')
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='None', max_length=32)
    specialty_id = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(signals.post_save, sender=User)
def new_doctor_account_emails(sender, instance, **kwargs):
    if instance.is_doctor:
        # Doctor welcome email
        lang = translation.get_language()
        translation.activate(lang)
        subject = _("Thank you for registering with us")
        message = _(f'Hi Dr. %(username)s, thank you for registering in the reservations system. your account will be activated soon by the admin.') % {'username': instance.username}
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, email_from, recipient_list)

        # Admin activate doctor account request email
        lang = translation.get_language()
        translation.activate(lang)
        subject = _("New Doctor Account ")
        message = _(f'Hi admin , there is new doctor registration account / need to check and activate / username: %(username)s') % {'username': instance.username}
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, email_from, recipient_list)


from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.utils import translation
from base.models import User
from .specialty import Specialty


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=15)
    photo = models.ImageField(upload_to='doctors/dr_pics', blank=True, default=None)
    degree_copy = models.ImageField(upload_to='doctors/dr_degree_copy', default=None)
    gender = models.CharField(choices=[('M', _('Male')), ('F', _('Female'))], default='None', max_length=32)
    specialty_id = models.ForeignKey(Specialty, on_delete=models.CASCADE, null=True)
    language = models.CharField(choices=[('ar', _('Arabic')), ('en', _('English'))], default='en', max_length=32)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(signals.post_save, sender=User)
def new_doctor_account_emails(sender, instance, **kwargs):
    if instance.is_doctor:
        # Doctor welcome email
        lang = translation.get_language()
        translation.activate(lang)
        subject = _('email_title')
        message = _('email_message')
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, email_from, recipient_list)

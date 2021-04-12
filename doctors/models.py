from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=100)
    phone = models.IntegerField(unique=True, default='00000000')
    photo = models.ImageField(upload_to='doctors/dr_pics', blank=True, default='')
    degree_copy = models.ImageField(upload_to='doctors/dr_degree_copy', default=' ')
    gender = models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='None', max_length=32)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        Doctor.objects.create(user=instance)

        subject = "Thank you for registering with us"
        message = f'Hi Dr. {instance.username}, thank you for registering in the reservations system. your account ' \
                  f'will be activated soon by the admin.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, email_from, recipient_list)


@receiver(signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.doctor.save()

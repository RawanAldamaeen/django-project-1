# Generated by Django 3.2 on 2021-04-26 10:42
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0001_initial'),
    ]

    operations = [
            migrations.CreateModel(
                name='Doctor',
                fields=[
                    (
                    'id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=100, unique=True)),
                    ('phone', models.CharField(max_length=15, unique=True)),
                    ('photo', models.ImageField(blank=True, default=None, upload_to='doctors/dr_pics')),
                    ('degree_copy', models.ImageField(default=None, upload_to='doctors/dr_degree_copy')),
                    ('gender',
                     models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='None', max_length=32)),
                    ('language',
                     models.CharField(choices=[('ar', 'Arabic'), ('en', 'English')], default='en', max_length=32)),
                    ('specialty_id',
                     models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctors.specialty')),
                    ('user',
                     models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ],
            ),
    ]

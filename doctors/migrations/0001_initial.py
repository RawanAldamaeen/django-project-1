# Generated by Django 3.2 on 2021-04-27 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty_en', models.CharField(max_length=100)),
                ('specialty_ar', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]

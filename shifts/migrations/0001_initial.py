# Generated by Django 3.2 on 2021-04-17 20:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_day', models.BooleanField(default=False)),
                ('start_time', models.CharField(blank=True, default=' ', max_length=20, validators=[django.core.validators.RegexValidator(regex='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]\\s?(?:AM|PM|am|pm)')])),
                ('end_time', models.CharField(blank=True, default=' ', max_length=20, validators=[django.core.validators.RegexValidator(regex='^([0-1]?[0-9]|2[0-3]):[0-5][0-9]\\s?(?:AM|PM|am|pm)')])),
                ('day', models.CharField(choices=[('Sun', 'Sunday'), ('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wen', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday'), ('Sat', 'Saturday')], default=' ', max_length=10)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.doctor')),
            ],
        ),
    ]

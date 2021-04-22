# Generated by Django 3.2 on 2021-04-21 09:20

from django.db import migrations


def load_data(apps, schema_editor):
    specialty = apps.get_model("base", "Specialty")

    specialty(specialty='Nurse', specialty_ar='مُمَرِّض').save()
    specialty(specialty='Ophthalmologist', specialty_ar='دكتور عيون').save()
    specialty(specialty='Dentist', specialty_ar='طبيب اسنان').save()
    specialty(specialty='Otolaryngologist', specialty_ar='طبيب انف اذن حنجرة').save()
    specialty(specialty='Neurologist', specialty_ar='طبيب اعصاب').save()
    specialty(specialty='Pediatrician', specialty_ar='طبيب اطفال').save()



class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_specialty_specialty_ar'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]

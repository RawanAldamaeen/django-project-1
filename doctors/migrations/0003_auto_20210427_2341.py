<<<<<<< HEAD:doctors/migrations/0003_auto_20210427_2341.py
# Generated by Django 3.2 on 2021-04-27 23:41
=======
# Generated by Django 3.2 on 2021-04-27 08:54
>>>>>>> cffb2cc85ddbfa4bf76fbad861312420008afc04:doctors/migrations/0003_auto_20210427_0854.py

from django.db import migrations

def load_data(apps, schema_editor):
    specialty = apps.get_model("doctors", "Specialty")

    specialty(specialty_en='Nurse', specialty_ar='مُمَرِّض').save()
    specialty(specialty_en='Ophthalmologist', specialty_ar='دكتور عيون').save()
    specialty(specialty_en='Dentist', specialty_ar='طبيب اسنان').save()
    specialty(specialty_en='Otolaryngologist', specialty_ar='طبيب انف اذن حنجرة').save()
    specialty(specialty_en='Neurologist', specialty_ar='طبيب اعصاب').save()
    specialty(specialty_en='Pediatrician', specialty_ar='طبيب اطفال').save()

<<<<<<< HEAD:doctors/migrations/0003_auto_20210427_2341.py
=======

>>>>>>> cffb2cc85ddbfa4bf76fbad861312420008afc04:doctors/migrations/0003_auto_20210427_0854.py
class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0002_auto_20210427_2340'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]

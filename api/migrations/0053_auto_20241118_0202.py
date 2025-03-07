# Generated by Django 5.0.3 on 2024-11-17 18:02

from django.db import migrations


def populate_profile(apps, schema_editor):
    IndividualRecordForm = apps.get_model('api', 'IndividualRecordForm')
    Profile = apps.get_model('api', 'Profile')

    default_profile = Profile.objects.first()  # Replace with appropriate logic
    for record in IndividualRecordForm.objects.filter(profile__isnull=True):
        record.profile = default_profile
        record.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_alter_individualrecordform_profile'),
    ]

    operations = [
        migrations.RunPython(populate_profile),
    ]

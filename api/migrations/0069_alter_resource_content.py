# Generated by Django 5.0.3 on 2025-02-04 00:58

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0068_alter_appointment_end_alter_appointment_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compile', '0002_auto_20211006_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmdupload',
            name='dosbox_output_file',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
    ]

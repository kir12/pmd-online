# Generated by Django 3.2.8 on 2021-10-06 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pmdupload',
            name='m2_filename',
        ),
        migrations.AddField(
            model_name='pmdupload',
            name='internal_filename',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='pmdupload',
            name='returned_m2_filename',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]

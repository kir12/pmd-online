# Generated by Django 3.2.8 on 2021-11-05 19:36

import compile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compile', '0005_pmdupload_ff_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pmdupload',
            name='ff_file',
            field=models.FileField(blank=True, null=True, upload_to=compile.models.save_path),
        ),
    ]
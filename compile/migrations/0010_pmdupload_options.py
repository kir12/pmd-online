# Generated by Django 4.2.5 on 2023-09-12 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compile', '0009_remove_pmdupload_dosbox_output_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmdupload',
            name='options',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
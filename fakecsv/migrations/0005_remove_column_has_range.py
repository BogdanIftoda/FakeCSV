# Generated by Django 3.1.7 on 2021-08-31 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fakecsv', '0004_auto_20210830_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='has_range',
        ),
    ]

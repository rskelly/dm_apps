# Generated by Django 2.2.2 on 2020-05-14 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0018_auto_20200513_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='trip_purpose',
        ),
    ]

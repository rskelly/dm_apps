# Generated by Django 2.2.2 on 2020-04-06 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spring_cleanup', '0003_auto_20200406_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='route',
            name='name_fr',
        ),
    ]

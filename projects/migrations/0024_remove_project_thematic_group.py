# Generated by Django 2.2.2 on 2020-01-08 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0023_auto_20200108_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='thematic_group',
        ),
    ]
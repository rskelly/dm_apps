# Generated by Django 2.2.2 on 2020-06-22 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_auto_20200622_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='distribution_format',
        ),
    ]

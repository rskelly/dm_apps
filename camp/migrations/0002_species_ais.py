# Generated by Django 2.1.4 on 2019-03-25 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='ais',
            field=models.BooleanField(default=False, verbose_name='Aquatic invasive species'),
        ),
    ]
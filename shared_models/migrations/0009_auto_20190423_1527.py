# Generated by Django 2.1.4 on 2019-04-23 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0008_auto_20190423_1526'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='port',
            unique_together={('province_code', 'district_code', 'port_code')},
        ),
    ]
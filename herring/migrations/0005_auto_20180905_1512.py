# Generated by Django 2.0.4 on 2018-09-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herring', '0004_auto_20180905_1512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lengthbin',
            name='id',
        ),
        migrations.AlterField(
            model_name='lengthbin',
            name='bin_length_cm',
            field=models.FloatField(primary_key=True, serialize=False),
        ),
    ]

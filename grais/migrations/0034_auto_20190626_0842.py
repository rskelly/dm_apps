# Generated by Django 2.2.2 on 2019-06-26 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0033_auto_20190620_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gcsample',
            name='traps_fished',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Traps fished (yyyy-mm-dd hh:mm)'),
        ),
        migrations.AlterField(
            model_name='gcsample',
            name='traps_set',
            field=models.DateTimeField(verbose_name='Traps set (yyyy-mm-dd hh:mm)'),
        ),
    ]
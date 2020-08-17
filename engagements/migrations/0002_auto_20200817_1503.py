# Generated by Django 2.2.2 on 2020-08-17 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engagements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='profit_nonprofit',
            field=models.PositiveIntegerField(blank=True, choices=[(None, '----'), (1, 'Profit'), (0, 'Non-Profit')], default=None, null=True, verbose_name='Profit/Non-Profit'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-29 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0009_auto_20200824_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='amount_owing',
            field=models.IntegerField(blank=True, choices=[(None, '---------'), (1, 'Yes'), (0, 'No')], null=True, verbose_name='does any funding need to be recovered?'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='funding_needed',
            field=models.IntegerField(blank=True, choices=[(None, '---------'), (1, 'Yes'), (0, 'No')], null=True, verbose_name='is funding needed?'),
        ),
    ]

# Generated by Django 2.1.4 on 2019-02-15 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0042_remove_entry_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='region',
            field=models.ManyToManyField(related_name='entries', to='ihub.Region'),
        ),
    ]

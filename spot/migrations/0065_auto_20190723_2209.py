# Generated by Django 2.2.2 on 2019-07-24 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0064_project_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='regional_score',
            field=models.FloatField(blank=True, null=True, verbose_name='regional score'),
        ),
    ]

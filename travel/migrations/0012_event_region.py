# Generated by Django 2.2.2 on 2019-10-29 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0025_region_head'),
        ('travel', '0011_auto_20191024_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips', to='shared_models.Region', verbose_name='DFO region'),
        ),
    ]

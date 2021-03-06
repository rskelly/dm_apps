# Generated by Django 3.1.2 on 2020-11-02 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0024_auto_20201102_1135'),
        ('projects', '0019_auto_20201102_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencematerial',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reference_materials', to='shared_models.region', verbose_name='region'),
        ),
    ]

# Generated by Django 3.1.2 on 2020-11-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects2', '0002_auto_20201109_0821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectyear',
            old_name='abl_services_required',
            new_name='requires_abl_services',
        ),
        migrations.AlterField(
            model_name='projectyear',
            name='data_storage_plan',
            field=models.TextField(blank=True, null=True, verbose_name='Data storage / archiving plan'),
        ),
    ]
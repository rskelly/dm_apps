# Generated by Django 2.0.4 on 2018-11-08 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['province', 'site']},
        ),
        migrations.RenameField(
            model_name='province',
            old_name='abbrev_eng',
            new_name='abbrev',
        ),
        migrations.RenameField(
            model_name='site',
            old_name='site_eng',
            new_name='site',
        ),
        migrations.RemoveField(
            model_name='province',
            name='abbrev_fre',
        ),
        migrations.RemoveField(
            model_name='site',
            name='site_fre',
        ),
    ]

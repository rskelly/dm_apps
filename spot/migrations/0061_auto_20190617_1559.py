# Generated by Django 2.2.2 on 2019-06-17 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0060_auto_20190617_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['type']},
        ),
        migrations.RenameField(
            model_name='file',
            old_name='date_uploaded',
            new_name='date_modified',
        ),
    ]
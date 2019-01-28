# Generated by Django 2.1.4 on 2019-01-28 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lineobject',
            old_name='description',
            new_name='description_eng',
        ),
        migrations.RenameField(
            model_name='lineobject',
            old_name='name',
            new_name='name_eng',
        ),
        migrations.AddField(
            model_name='lineobject',
            name='code',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]

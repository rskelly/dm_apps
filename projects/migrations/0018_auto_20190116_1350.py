# Generated by Django 2.1.4 on 2019-01-16 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_division_name_fr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='division',
            old_name='name_fr',
            new_name='nom',
        ),
    ]
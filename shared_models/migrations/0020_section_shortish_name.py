# Generated by Django 3.1.2 on 2020-10-29 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0019_auto_20201028_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='shortish_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='shortish name'),
        ),
    ]

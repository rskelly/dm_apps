# Generated by Django 2.2.2 on 2020-05-14 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0011_auto_20200513_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purpose',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='purpose',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

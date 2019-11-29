# Generated by Django 2.2.2 on 2019-10-21 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20190816_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='fgp_url',
            field=models.URLField(blank=True, null=True, verbose_name='Link to record on FGP'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='public_url',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Link to record on Open Data'),
        ),
    ]
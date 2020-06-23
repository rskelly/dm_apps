# Generated by Django 2.2.2 on 2020-05-08 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmutools', '0013_auto_20200508_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='supplier',
            field=models.ManyToManyField(blank=True, related_name='suppliers', to='mmutools.Supplier', verbose_name='supplier'),
        ),
    ]
# Generated by Django 2.2.2 on 2019-06-26 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scifi', '0009_auto_20190626_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='consignee_suffix',
            field=models.IntegerField(blank=True, null=True, verbose_name='consignee suffix'),
        ),
    ]
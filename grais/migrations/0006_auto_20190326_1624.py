# Generated by Django 2.1.4 on 2019-03-26 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0005_auto_20190326_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='code',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 2.2.2 on 2020-01-24 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_auto_20200124_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='is_group_request',
            field=models.BooleanField(default=False, verbose_name='Is this a group request (i.e., a request for multiple individuals)?'),
        ),
    ]

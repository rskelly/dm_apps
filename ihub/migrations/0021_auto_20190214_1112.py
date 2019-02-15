# Generated by Django 2.1.4 on 2019-02-14 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ihub', '0020_auto_20190214_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='current_chief',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='election_date',
        ),
        migrations.AddField(
            model_name='organization',
            name='next_election',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
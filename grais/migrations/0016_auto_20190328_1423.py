# Generated by Django 2.1.4 on 2019-03-28 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0015_auto_20190328_1340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bycatch',
            options={'ordering': ['trap', 'species', 'id']},
        ),
        migrations.AlterModelOptions(
            name='crab',
            options={'ordering': ['trap', 'species', 'id']},
        ),
        migrations.AlterField(
            model_name='species',
            name='green_crab_monitoring',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='bycatch',
            unique_together=set(),
        ),
    ]
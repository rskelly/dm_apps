# Generated by Django 2.1.4 on 2019-05-22 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_auto_20190517_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='project',
            name='deliverables',
            field=models.TextField(blank=True, null=True, verbose_name='Project deliverables'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_competitive',
            field=models.NullBooleanField(default=False, verbose_name='Is the funding competitive?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_negotiable',
            field=models.NullBooleanField(choices=[(None, 'Unknown'), (True, 'Negotiable'), (False, 'Non-negotiable')], verbose_name='Negotiable or non-negotiable?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='priorities',
            field=models.TextField(blank=True, null=True, verbose_name='Project-specific priorities'),
        ),
    ]

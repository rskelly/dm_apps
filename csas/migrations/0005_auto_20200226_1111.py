# Generated by Django 2.2.2 on 2020-02-26 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csas', '0004_auto_20200226_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metmeeting',
            name='csas_contact',
            field=models.ManyToManyField(related_name='csas_contacts', to='csas.ConContact'),
        ),
        migrations.AlterField(
            model_name='metmeeting',
            name='other_region',
            field=models.ManyToManyField(related_name='other_regions', to='shared_models.Region'),
        ),
        migrations.AlterField(
            model_name='metmeeting',
            name='program_contact',
            field=models.ManyToManyField(related_name='program_contacts', to='csas.ConContact'),
        ),
    ]

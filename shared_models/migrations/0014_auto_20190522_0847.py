# Generated by Django 2.1.4 on 2019-05-22 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0013_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='branches', to='shared_models.Region', verbose_name='region'),
        ),
        migrations.AlterField(
            model_name='division',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='divisions', to='shared_models.Branch', verbose_name='branch'),
        ),
    ]
# Generated by Django 2.2.2 on 2020-06-17 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0007_auto_20200617_0856'),
        ('projects', '0014_upcomingdate_is_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upcomingdate',
            name='name',
        ),
        migrations.RemoveField(
            model_name='upcomingdate',
            name='nom',
        ),
        migrations.AddField(
            model_name='upcomingdate',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='project_upcoming_dates', to='shared_models.Region', verbose_name='region'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='upcomingdate',
            name='description_en',
            field=models.TextField(default=1, verbose_name='description (en)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='upcomingdate',
            name='description_fr',
            field=models.TextField(blank=True, null=True, verbose_name='description (fr)'),
        ),
    ]

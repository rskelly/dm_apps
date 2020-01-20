# Generated by Django 2.2.2 on 2019-12-16 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_auto_20191216_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='activity_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.ActivityType', verbose_name='activity type'),
        ),
        migrations.RemoveField(
            model_name='project',
            name='default_funding_source',
        ),
        migrations.AddField(
            model_name='project',
            name='default_funding_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='projects.FundingSource', verbose_name='default funding source'),
        ),
        migrations.AlterField(
            model_name='project',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='projects', to='shared_models.Section', verbose_name='section'),
        ),
    ]
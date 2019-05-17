# Generated by Django 2.1.4 on 2019-05-06 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spot', '0013_auto_20190506_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributionagreementchecklist',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='contributionagreementchecklist',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ca_checklist_last_mods', to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='expressionofinterest',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='expressionofinterest',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='payment',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='payment',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='photo',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='uploaded'),
        ),
        migrations.AddField(
            model_name='project',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='project',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gc_projects', to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='projectyear',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='projectyear',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='report',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='report',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='reportchecklist',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='reportchecklist',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='report_checklist_mods', to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
        migrations.AddField(
            model_name='sitevisit',
            name='date_last_modified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='date last modified'),
        ),
        migrations.AddField(
            model_name='sitevisit',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='last modified by'),
        ),
    ]
# Generated by Django 2.1.4 on 2019-06-05 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0016_auto_20190605_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shared_models_branches', to=settings.AUTH_USER_MODEL, verbose_name='branch manager'),
        ),
        migrations.AddField(
            model_name='division',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shared_models_divisions', to=settings.AUTH_USER_MODEL, verbose_name='division manager'),
        ),
    ]
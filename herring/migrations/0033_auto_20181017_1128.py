# Generated by Django 2.0.4 on 2018-10-17 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('herring', '0032_auto_20181001_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fishdetail',
            name='ager',
        ),
        migrations.AddField(
            model_name='fishdetail',
            name='otolith_sampler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='otolith_sampler_fish_details', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fishdetailtest',
            name='field_name',
            field=models.CharField(choices=[(' global', ' global'), ('fish_weight', 'somatic weight'), ('gonad_weight', 'gonad weight'), ('fish_length', 'fish length'), ('annulus_count', 'annulus count')], max_length=55),
        ),
    ]
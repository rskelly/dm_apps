# Generated by Django 2.1.4 on 2019-01-08 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grais', '0032_sample_old_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='station',
            options={'ordering': ['station_name']},
        ),
        migrations.AlterField(
            model_name='station',
            name='province',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stations', to='grais.Province'),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.0.4 on 2018-11-09 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0004_station_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeciesObservations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_adults', models.IntegerField(default=0)),
                ('count_yoy', models.IntegerField(default=0)),
                ('count_unknown', models.IntegerField(default=0)),
                ('count_total', models.IntegerField(blank=True, null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sample_spp', to='camp.Sample')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sample_spp', to='camp.Species')),
            ],
        ),
        migrations.RemoveField(
            model_name='samplespecies',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='samplespecies',
            name='species',
        ),
        migrations.RemoveField(
            model_name='samplespecies',
            name='stage',
        ),
        migrations.DeleteModel(
            name='SampleSpecies',
        ),
        migrations.DeleteModel(
            name='Stage',
        ),
    ]
# Generated by Django 2.1.4 on 2019-03-26 19:15

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0004_auto_20190326_1212'),
        ('grais', '0004_auto_20190326_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estuary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GCProbeMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_date', models.DateTimeField(blank=True, null=True)),
                ('timezone', models.CharField(blank=True, choices=[('AST', 'AST'), ('ADT', 'ADT'), ('UTC', 'UTC')], max_length=5, null=True)),
                ('temp_c', models.FloatField(blank=True, null=True, verbose_name='temperature (°C)')),
                ('sal', models.FloatField(blank=True, null=True, verbose_name='salinity')),
                ('o2_percent', models.FloatField(blank=True, null=True, verbose_name='Dissolved oxygen (%)')),
                ('o2_mgl', models.FloatField(blank=True, null=True, verbose_name='Dissolved oxygen (mg/L)')),
                ('sp_cond_ms', models.FloatField(blank=True, null=True, verbose_name='Specific conductance (mS)')),
                ('cond_ms', models.FloatField(blank=True, null=True, verbose_name='Conductivity (mS)')),
                ('tide_state', models.CharField(blank=True, choices=[('h', 'High'), ('m', 'Mid'), ('l', 'Low')], max_length=5, null=True)),
                ('tide_direction', models.CharField(blank=True, choices=[('in', 'Incoming'), ('out', 'Outgoing')], max_length=5, null=True)),
                ('cloud_cover', models.IntegerField(blank=True, null=True, verbose_name='cloud cover (%)')),
                ('probe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grais.Probe')),
            ],
        ),
        migrations.CreateModel(
            name='GCSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trap_set', models.DateTimeField()),
                ('trap_fished', models.DateTimeField(blank=True, null=True)),
                ('season', models.IntegerField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('samplers', models.ManyToManyField(to='grais.Sampler')),
            ],
            options={
                'ordering': ['-trap_set', 'site'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('latitude_n', models.FloatField(blank=True, null=True)),
                ('longitude_w', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('estuary', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stations', to='grais.Estuary')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Trap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trap_number', models.IntegerField()),
                ('trap_type', models.IntegerField(choices=[(1, 'Fukui')], default=1)),
                ('bait_type', models.IntegerField(choices=[(1, 'Herring')], default=1)),
                ('latitude_n', models.FloatField(blank=True, null=True)),
                ('longitude_w', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('total_green_crab_wt_kg', models.FloatField(blank=True, null=True, verbose_name='Total weight of green crabs (kg))')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='traps', to='grais.GCSample')),
            ],
            options={
                'ordering': ['sample', 'trap_number'],
            },
        ),
        migrations.CreateModel(
            name='TrapSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('width', models.FloatField(blank=True, null=True)),
                ('carapace_color', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('abdomen_color', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('egg_color', models.CharField(blank=True, max_length=25, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='trap_spp', to='grais.Species')),
                ('trap', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='trap_spp', to='grais.Trap')),
            ],
        ),
        migrations.CreateModel(
            name='WeatherConditions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Province',
        ),
        migrations.AddField(
            model_name='gcsample',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='grais.Site'),
        ),
        migrations.AddField(
            model_name='gcprobemeasurement',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='probe_data', to='grais.GCSample'),
        ),
        migrations.AddField(
            model_name='gcprobemeasurement',
            name='weather_conditions',
            field=models.ManyToManyField(to='grais.WeatherConditions'),
        ),
        migrations.AddField(
            model_name='estuary',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='estuaries', to='shared_models.Province'),
        ),
        migrations.AlterUniqueTogether(
            name='trapspecies',
            unique_together={('species', 'trap')},
        ),
    ]

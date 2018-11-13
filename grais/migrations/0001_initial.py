# Generated by Django 2.0.7 on 2018-08-22 17:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import grais.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_number', models.CharField(max_length=55, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude_n', models.FloatField(blank=True, null=True)),
                ('longitude_w', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('collector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lines', to='grais.Collector')),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Probe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probe_name', models.CharField(max_length=255)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProbeMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_date', models.DateTimeField(blank=True, null=True)),
                ('tide_descriptor', models.CharField(blank=True, choices=[('eb', 'Ebb'), ('fl', 'Flood'), ('hi', 'High'), ('lo', 'Low')], max_length=2, null=True)),
                ('probe_depth', models.FloatField(blank=True, null=True)),
                ('temp_c', models.FloatField(blank=True, null=True)),
                ('sal_ppt', models.FloatField(blank=True, null=True)),
                ('o2_percent', models.FloatField(blank=True, null=True)),
                ('o2_mgl', models.FloatField(blank=True, null=True)),
                ('sp_cond_ms', models.FloatField(blank=True, null=True)),
                ('spc_ms', models.FloatField(blank=True, null=True)),
                ('ph', models.FloatField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('probe', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grais.Probe')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('abbrev', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_deployed', models.DateTimeField()),
                ('date_retrieved', models.DateTimeField(blank=True, null=True)),
                ('days_deployed', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('notes_html', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('season', models.IntegerField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-season', 'station', '-date_deployed'],
            },
        ),
        migrations.CreateModel(
            name='Sampler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name', models.CharField(blank=True, max_length=255, null=True)),
                ('scientific_name', models.CharField(blank=True, max_length=255, null=True)),
                ('abbrev', models.CharField(blank=True, max_length=255, null=True)),
                ('tsn', models.IntegerField(blank=True, null=True, verbose_name='ITIS TSN')),
                ('aphia_id', models.IntegerField(blank=True, null=True, verbose_name='AphiaID')),
                ('color_morph', models.BooleanField(verbose_name='Has color morph')),
                ('invasive', models.BooleanField()),
                ('biofouling', models.BooleanField()),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['common_name'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude_n', models.FloatField(blank=True, null=True)),
                ('longitude_w', models.FloatField(blank=True, null=True)),
                ('depth', models.FloatField(blank=True, null=True)),
                ('site_desc', models.TextField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='stations', to='grais.Province')),
            ],
            options={
                'ordering': ['province', 'station_name'],
            },
        ),
        migrations.CreateModel(
            name='Surface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surface_type', models.CharField(choices=[('pe', 'Petri dish'), ('pl', 'Plate')], max_length=2)),
                ('label', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=grais.models.img_file_name)),
                ('notes', models.TextField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='surfaces', to='grais.Line')),
            ],
            options={
                'ordering': ['line', 'surface_type', 'label'],
            },
        ),
        migrations.CreateModel(
            name='SurfaceSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_coverage', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('notes', models.TextField(blank=True, null=True)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='surface_spp', to='grais.Species')),
                ('surface', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='surface_spp', to='grais.Surface')),
            ],
        ),
        migrations.AddField(
            model_name='surface',
            name='species',
            field=models.ManyToManyField(through='grais.SurfaceSpecies', to='grais.Species'),
        ),
        migrations.AddField(
            model_name='sample',
            name='sampler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='grais.Sampler'),
        ),
        migrations.AddField(
            model_name='sample',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='grais.Station'),
        ),
        migrations.AddField(
            model_name='probemeasurement',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='probe_data', to='grais.Sample'),
        ),
        migrations.AddField(
            model_name='line',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lines', to='grais.Sample'),
        ),
        migrations.AlterUniqueTogether(
            name='surfacespecies',
            unique_together={('species', 'surface')},
        ),
    ]

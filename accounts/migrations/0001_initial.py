# Generated by Django 2.2.2 on 2019-10-17 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0025_region_head'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('position_fre', models.CharField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=25, null=True)),
                ('language', models.IntegerField(blank=True, choices=[(1, 'English'), (2, 'French')], null=True, verbose_name='language preference')),
                ('retired', models.BooleanField(default=False)),
                ('section', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shared_models.Section', verbose_name='Section')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__last_name', 'user__first_name'],
            },
        ),
    ]
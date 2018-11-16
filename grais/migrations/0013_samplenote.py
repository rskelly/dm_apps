# Generated by Django 2.0.4 on 2018-11-16 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grais', '0012_auto_20181116_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampleNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('note', models.TextField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='notes', to='grais.Sample')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]

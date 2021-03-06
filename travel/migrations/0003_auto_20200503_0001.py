# Generated by Django 2.2.2 on 2020-05-03 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0002_defaultreviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='status',
            field=models.ForeignKey(default=8, limit_choices_to={'used_for': 4}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips', to='travel.Status', verbose_name='trip status'),
        ),
        migrations.CreateModel(
            name='TripReviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(null=True, verbose_name='process order')),
                ('status_date', models.DateTimeField(blank=True, null=True, verbose_name='status date')),
                ('comments', models.TextField(null=True, verbose_name='Comments')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='travel.ReviewerRole', verbose_name='role')),
                ('status', models.ForeignKey(default=4, limit_choices_to={'used_for': 3}, on_delete=django.db.models.deletion.DO_NOTHING, to='travel.Status', verbose_name='review status')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewers', to='travel.Conference')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='trip_reviewers', to=settings.AUTH_USER_MODEL, verbose_name='DM Apps user')),
            ],
            options={
                'ordering': ['trip', 'order'],
                'unique_together': {('trip', 'user', 'role')},
            },
        ),
    ]

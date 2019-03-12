# Generated by Django 2.1.4 on 2019-03-12 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0006_auto_20190312_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='objective_of_event',
            field=models.TextField(blank=True, null=True, verbose_name='objective of the event (Brief description of what the event is about.  Not objective of the Participants in going to the event.)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='connected user'),
        ),
    ]
# Generated by Django 2.2.2 on 2020-01-24 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_auto_20200124_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triprequest',
            name='parent_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_requests', to='travel.TripRequest'),
        ),
    ]
# Generated by Django 2.2.2 on 2019-11-07 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0026_auto_20191106_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewer',
            name='order',
            field=models.IntegerField(blank=True, null=True, verbose_name='process order'),
        ),
        migrations.AlterField(
            model_name='status',
            name='used_for',
            field=models.IntegerField(choices=[(1, 'Reviewer status'), (2, 'Trip status')]),
        ),
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.ForeignKey(default=8, limit_choices_to={'used_for': 2}, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips', to='travel.Status', verbose_name='trip status'),
        ),
    ]